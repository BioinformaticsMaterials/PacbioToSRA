import sys
import time
import pyfaspmgmt
import os

files = ['/home/bear/test/0','/home/bear/test/1', '/home/bear/test/2']
dst = ['3','4','5']

print "Generating file list"
files = os.listdir("h:/bear/test/100k001")

#files = map ( lambda x: "<File><Filename>H:/bear/test/100k001/%s</Filename><FileType>media</FileType></File>" % x, files )
files = map ( lambda x: "H:/bear/test/10k002/%s" % x, files )
#print "\n".join(files)
#exit()
files = files[:200]
print "Transfer Starting."

session = pyfaspmgmt.FaspSend(
  "avidtest",
  "192.168.56.101",
  src_files=files,
  dest_dir="E:/foo",
  password="LZPJXxLDgv9i",
  args = ['--precalculate-job-size','-l', '250000', '-L','.', '-S-', '-P', "33333" ], old=True )

time.sleep(1)
#session.cancel()

while session.isRunning():
  sys.stdout.write("\r%02d%% Complete" % session.pctComplete() )
  time.sleep(.5)
  sys.stdout.flush()

print ""

if session.status() == "DONE":
  print "File Transfer Successful"
else:
  print "\n".join(session.errs)
  print "Transfer Failed"

print "Exiting..."
