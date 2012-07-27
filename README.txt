
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



Enjoy!

