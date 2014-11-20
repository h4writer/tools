import sys
#import jsbeautifier
import os
from Reducer import *

if len(sys.argv) != 5:
    print "Usage:", sys.argv[0], "[Path to buggy js]", "[Path to non-buggy js]", "[Path to testcase]", "[Word that buggy js parser will output, but not normal js parser won't]"
    exit()

# info about the reducing
info = {
    "failing_js": sys.argv[1],
    "js": sys.argv[2],
    "original_test": sys.argv[3],
    "reduced_test": "/run/shm/"+sys.argv[3].split("/")[-1]+".reduced",
    "temp_test": "/run/shm/"+sys.argv[3].split("/")[-1]+".tmp",
    "verification": sys.argv[4] 
}

print "JS reducer"
print "Buggy JS parser:\t", info["failing_js"]
print "JS parser:\t\t", info["js"]
print "Testcase:\t\t", info["original_test"]
print "Word indicating bug still present:\t", info["verification"]
print ""

# Test if testcase fails on buggy_js
"""output = Utils.run(info["failing_js"], info["original_test"])
if output == -1:
    exit("Couldn't run the buggy js parser")
if not Utils.verify(output, info["verification"]):
    exit("Testcase doesn't trigger bug on buggy js parser")

output = Utils.run(info["js"], info["original_test"])
if output == -1:
    exit("Couldn't run normal js parser")
if Utils.verify(output, info["verification"]):
    exit("Testcase triggers bug on normal js parser")"""

# Format text in a better way
print "Formatting JS testcase"
if os.path.exists(info["reduced_test"]):
    print "Already done"
else:
    f = open(info["original_test"], 'r')
    data = "\r".join(f.readlines());
    f.close()

    f = open(info["reduced_test"], 'w')
    #f.write(jsbeautifier.beautify(data))
    f.write(data)
    f.close()
# TODO: change , of vars into ;
# TODO: change ()? : into if() {} else {} construction

# Test integrity reduced testcase
output = Utils.run(info["failing_js"], info["reduced_test"])
if output == -1:
    exit("Reduced testcase gives an error when run.")
if not Utils.verify(output, info["verification"]):
    exit("Reduced testcase doesn't trigger bug on buggy js parser.")

output = Utils.run(info["js"], info["reduced_test"])
if output == -1:
    exit("Reduced testcase gives an error when run.")
if Utils.verify(output, info["verification"]):
    exit("Reduced testcase triggers bug on normal js parser")

# Reduce
f = open(info["reduced_test"], 'r')
lines = len(f.readlines());
f.close()

script = Script(info)
reducer = Reducer(script)
#reducer.start()


import random
while 1:
  length = random.randint(0, 5)+1
  line = random.randint(0, len(reducer.script.lines)-5)
  print line, line+length
  lines = reducer.script.lines
  reducer.line1(line, line+length)
"""

for i in range(100, 0, -1):
  #for j in range(lines/i):
  for j in range(lines/i, 0, -1):
      print j*i, (j+1)*i
      reducer.line(j*i, (j+1)*i)
reducer.line(0, lines)
"""

print lines,
f = open(info["reduced_test"], 'r')
lines = len(f.readlines());
f.close()
print "=>", lines

