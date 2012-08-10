This is a tool to automatically fetch/clone all repositories on github and
bitbucket into a local folder using the service APIs.

The services are configured through the config file 'repomess.ini', here is an
example:

  [GitHub]
  path = gh/%%(publicprivate)s/%%(slug)s/
  username = 0x01
  password = s3cr3t_1
  
  [Bitbucket]
  path = bb/%%(publicprivate)s/%%(slug)s/
  username = wires
  password = s3cr3t_2

(if you have a % in your password you need to escape it with %)

Then just run the program:

  python repomess.py

And it will clone or update into

 gh/public/myrepo1/
 bb/private/myrepo2/

Etc...

Enjoy!

PS. many things can be improved, help is welcome

SOME THINGS I'D LIKE TO ADD:
 
 - Specify manual repository urls
 - Parallel cloning/fetching
 - Daemon mode with notifications of incoming changesets
 - Improved security (no plaintext pass)
 - At least only run in conf file has 600 permission
 - etc...