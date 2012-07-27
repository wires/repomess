import json, urllib2, base64

class GitHub:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def apicall(self, q):
        # get user's repositories
        request = urllib2.Request("https://api.github.com/%s" % q)

        # HTTP Basic auth
        p = base64.encodestring('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % p)
    
        # do http call
        result = urllib2.urlopen(request)

        # parse JSON result and return
        return json.load(result)

    def repos(self):
        repos = self.apicall("user/repos?page=1&per_page=100")

        f = lambda s: ('git', s["git_url"], s["name"], s["private"])

        # return the list of git_urls
        return map(f, repos)


class Bitbucket:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def apicall(self, q):
        # get user's repositories
        request = urllib2.Request("https://api.bitbucket.org/1.0/%s" % q)

        # HTTP Basic auth
        p = base64.encodestring('%s:%s' % (self.username, self.password))
        request.add_header("Authorization", "Basic %s" % p)
    
        # do http call
        result = urllib2.urlopen(request)
        
        return json.load(result)

    def repos(self):
        # parse and return json as python object
        def fn(s):
            private = s['is_private']
            slug = s['slug']
            scm = s['scm']
            u = self.username

            if scm == 'git':
                uri = 'git@bitbucket.org:%s/%s.git' % (u, slug)

            if scm == 'hg':
                uri = 'ssh://hg@bitbucket.org/%s/%s' % (u, slug)

            return (scm, uri, slug, private)

        response = self.apicall("users/%s" % self.username)

        return map(fn, response["repositories"])


class Scm:
    def __init__(self, uri, dest):
        self.executable = self.__class__.__name__
        self.uri = uri
        self.dest = dest

    def run_cmd(self, cmd):
        c = [self.executable] + cmd
        print ' '.join(c)
        subprocess.call(c, cwd=self.dest)

class git(Scm):
    def clone(self):
        self.run_cmd(['clone', self.uri, '.'])

    def fetch(self):
        self.run_cmd(['fetch', self.uri])
        
class hg(Scm):
    def clone(self):
        self.run_cmd(['clone', self.uri, '.'])

    def fetch(self):
        self.run_cmd(['pull', self.uri])


import sys, os, getopt, pprint, subprocess
from ConfigParser import SafeConfigParser

pp = pprint.PrettyPrinter(indent=3)

def run_service(service, **conf):
        # construct the API wrapper for this service
        host = eval("%s('%s', '%s')" % (service, conf['username'], conf['password']))

        # query service for a list of repositories
        repos = host.repos()

        # clone or update each repo
        for scm_str, uri, slug, private in repos:
            d = {}
            d['scm'] = scm_str
            d['uri'] = uri
            d['slug'] = slug
            d['publicprivate'] = private and 'private' or 'public'

            # interpolate configured destination
            dest = conf['path'] % d

            if not scm_str in ['hg','git']:
                continue

            # construct SCM api wrapper
            scm = eval("%s('%s','%s')" % (scm_str, uri, dest))

            if not os.path.exists(dest):
                # clone into fresh directory
                os.makedirs(dest)
                scm.clone()
            else:
                # update existing repository
                scm.fetch()


def conf_check(service, **conf):
    # only defined services are possible
    if not service in ['GitHub','Bitbucket']:
        print "Unknown service %s" % service
        return False
            
    # we need username and password
    for option in ['username', 'password']:
        if not conf.has_key(option):
            print "Missing required %s option" % option
            return False

    return True

# process all repositories
if __name__ == "__main__":

    # read config file
    parser = SafeConfigParser()
    parser.read('repomess.ini')

    # each section defines a service
    for service in parser.sections():

        # dictionary of currect section's config option
        conf = dict(parser.items(service))

        # check configuration
        if not conf_check(service, **conf):
            continue

        # run service
        run_service(service, **conf)
