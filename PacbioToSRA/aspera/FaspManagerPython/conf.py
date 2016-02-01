import ConfigParser
import datetime
import time
import random
import binascii
import struct
import os
import subprocess

try: 
  import vers
  DATE=vers.DATE
  VERSION=vers.VERSION
  ASCP=vers.ASCP
except:
  DATE="NA"
  VERSION="NA"
  ASCP='ascp'

WIN_ASCP_PATH = [ 
  "C:/Program Files (x86)/Aspera/Enterprise Server/bin", 
  "C:/Program Files/Aspera/Enterprise Server/bin",
  "C:/Program Files/Aspera/Point-to-Point/bin",
  "C:/Program Files (x86)/Aspera/Point-to-Point/bin"]

  

configPaths = [ "C:/Program Files (x86)/Aspera/wanaccel/faspmgmt.conf", 
                "C:/Program Files/Aspera/wanaccel/faspmgmt.conf", 
		"faspmgmt.conf" ]
error = []
cfg = None
configFile = ""

def writeConfig():
  try:
    cfg.set("all","sessionNo", 1+int(cfg.get("all", "sessionNo")) )
  except:
    cfg.set("all","sessionNo", 1 )
  cfg.set("all","now", int(time.mktime(datetime.datetime.utcnow().utctimetuple())) )
  cfg.set("all","currentPid", os.getpid() )
  try: 
    with open(configFile, "wb") as fp:
      cfg.write(fp)
  except:
    for i in configPaths: 
      try:
        with open(i, "wb") as fp:
          cfg.write(fp)
        break
      except:
        pass


def readConfig( path ):
  global cfg
  c = ConfigParser.RawConfigParser({}) 
  with open(path) as fp:
    c.readfp(fp)
  cfg = c
  now = int(time.mktime(datetime.datetime.utcnow().utctimetuple()))
  if ( (int(cfg.get("all", "currentPid")) != os.getpid()) or
       (now - int(cfg.get("all", "now")) > 60)  ):
    writeConfig()
    reReadConfig()
  return cfg

foundConf = False

def reReadConfig():
  global configFile
  for p in configPaths:
    try: 
      cfg = readConfig(p)
      global foundConf
      if not foundConf:
        # print "Using config from:", p
        foundConf = True
      if cfg:
        configFile = p
        break
    except IOError, e:
      error.append("{%s->%s}" % (e.filename, e.strerror) )
    except Exception, e:
      error.append("{%s->%s}" % (p, e.message))

reReadConfig()

if not cfg:
  cfg = ConfigParser.RawConfigParser({}) 
  rand = random.SystemRandom()
  epoch = int(time.mktime(datetime.datetime.utcnow().utctimetuple()))
  epoch = binascii.b2a_base64(struct.pack('I', epoch))[:6]
  sysId = binascii.b2a_base64(struct.pack('Q', rand.getrandbits(48) ))[:8]

  cfg.add_section("all")
  cfg.set("all","sysId", "%s-%s" % (sysId, epoch) )
  path = os.path.dirname( configFile )
  cfg.set("all","installPath", os.getcwd())
  ascp_path = False
  try: 
    ascp_path = subprocess.check_output(["which", ASCP]).strip()
  except:
    pass

  if not ascp_path:
    for path in WIN_ASCP_PATH:
      # print "%s/%s" % (path, ASCP)
      if os.path.isfile( "%s/%s.exe" % (path, ASCP) ): 
        ascp_path = "%s/%s.exe" % (path, ASCP)
        break

  cfg.set("all","ascpPath", ascp_path)

  writeConfig()
  reReadConfig()

try:
  if cfg.get("all", "debug").lower() == "true":
    import pdb
    import sys 

    def debugger(type, value, tb):
        pdb.pm()
    sys.excepthook = debugger
    print "Debugging Enabled"

 
except:
  pass


