#!/usr/bin/python

import sys
import time
import pyfaspmgmt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("user", help="username", nargs=1)
parser.add_argument("host", help="remotehost", nargs=1)
parser.add_argument("--ascpRoot", help="ascp root", nargs='?', default=None)
parser.add_argument("file", help="files to send", 
                            nargs='+', type=file)
try:
  import argcomplete
  argcomplete.autocomplete(parser)
except:
  pass

res = parser.parse_args(sys.argv[1:])

files = [ x.name for x in res.file ] 
[ x.close() for x in res.file ]

sys.stdout.write("Password: ")
password = sys.stdin.readline()
password = password[:-1]

print res.user

session = pyfaspmgmt.FaspSend(
  res.user[0],
  res.host[0],
  src_files=files,
  dest_dir=".",
  password=password,
  ascpRoot=res.ascpRoot,
  args = ['--precalculate-job-size','-l', '250000', '-L','.', '-S-', '-P', "33333" ], old=True )

time.sleep(.5)

while session.status() not in ("DONE", "ERROR"):
  time.sleep(.5)
  sys.stdout.write("\r%02d%% Complete" % session.pctComplete() )
  sys.stdout.flush()

print ""

if session.status() == "DONE":
  print "File Transfer Successful"
else:
  print "Transfer Failed"
  print "\n".join(session.errs)

print "Exiting..."
