import sys
import time
import pyfaspmgmt

files = ['test/1M','test/100k', 'test/300k']
dst = ['3','4','5']

session = pyfaspmgmt.FaspSend(
  "avidtest",
  "66.211.105.167",
  persistent=True,
  password="LZPJXxLDgv9i",
  args = ['--precalculate-job-size',] )


for pair in zip(files, dst):
  session.addFile(*pair)

session.closePersistentSession()
  

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
