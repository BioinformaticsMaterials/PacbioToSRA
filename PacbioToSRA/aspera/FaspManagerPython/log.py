# -*- coding: utf-8 -*-
import logging
import logging.handlers
import sys
import traceback

from conf import cfg

logger=False
loglevel="INFO"

#loglevel="INFO" # Default setting for shipping product.
doDebug = False
def info(message):
  log(message, "info")

def err(message):
  log(message, "error")

def log(message, urgency="error"):
  global logger, doDebug

  try:
    if not logger:

      loglevel = "INFO"
      try:
        if "true" in cfg.get("all", "debug").lower(): 
          loglevel = "DEBUG"
        doDebug = True
      except:
        pass

      maxBytes=10485760
      backupCount=10
      fmt ="%(asctime)s %(levelname)s %(message)s" 
      datefmt= "%Y%m%d-%H%M%S"

      fn = "faspmgmt.log"
      try: 
        fn = cfg.get("all", "logname")
      except:
        pass

      try:
        loglevel = cfg.get("all", "loglevel")
        fmt = cfg.get("all", "logformat")
        datefmt= cfg.get("all", "logdateformat")
      except:
        pass

      fn = "%s/%s" % (cfg.get("all", "installPath"), fn)
 
      logger=logging.getLogger("pyFaspMgmt")
      handler = logging.handlers.RotatingFileHandler( fn,
          maxBytes=maxBytes, backupCount=backupCount)
      handler.setFormatter( logging.Formatter(fmt, datefmt) )
      logger.addHandler(handler)
      logger.setLevel( loglevel )
    if doDebug:
      print message
    getattr(logger, urgency)(message)
    if urgency == "error":
      getattr(logger, urgency)(printtb())
  except Exception, e:
    print "LOGGER ERROR: ", e
  return message

def dbg( arg ):
  log( arg, "debug" )

def printtb():
  try: 
    fail_line=sys.exc_traceback.tb_lineno
    t,v,tb=sys.exc_info()
    traceback.print_tb(tb)
    l = traceback.extract_tb(tb)
    return traceback.format_list(l)
  except:
    return "No TB"



 

