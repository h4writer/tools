import sys
#import python.jsbeautifier
import os
from Reducer import *

if len(sys.argv) != 4:
    print "Usage:", sys.argv[0], "[Path to buggy js]", "[Path to non-buggy js]", "[Path to testcase]"
    exit()

# info about the reducing
info = {
    "failing_js": sys.argv[1],
    "js": sys.argv[2],
    "original_test": sys.argv[3],
    "reduced_test": "/run/shm/"+sys.argv[3].split("/")[-1]+".reduced",
    "temp_test": "/run/shm/"+sys.argv[3].split("/")[-1]+".tmp",
    "verification": ""
}

print "JS reducer"
print "Buggy JS parser:\t", info["failing_js"]
print "JS parser:\t\t", info["js"]
print "Testcase:\t\t", info["original_test"]
print ""

def test(self, buggy_js, js, tmp, verification):
    output = Utils.run(buggy_js, tmp)
    if output == -1:
        return False

    output2 = Utils.run(js, tmp)
    if output2 == -1:
        return False;

    if "SyntaxError:" in output2 and "SyntaxError:" in output:
        return False

    if "ReferenceError:" in output2 and "ReferenceError:" in output:
        return False

    if "TypeError:" in output2 and "TypeError:" in output:
        return False

    if output == "" or output == "":
        return False

    time = Utils.numeric(output)
    time2 = Utils.numeric(output2)

    if abs(time - time2) < 0.1:
        return False

    if time*1./time2 > 1.20:
        print time*1./time2
        return True

    #if not present(output, output2):
    #    return False

    return False

Utils.test = classmethod(test)

def present(output1, output2):
    print info["failing_js"]
    print output1
    print Utils.numeric(output1)

    print info["js"]
    print output2
    print Utils.numeric(output2)

    print "--------------------------"
    print Utils.numeric(output1)*1./Utils.numeric(output2)
    present = raw_input("Is bug still present? (y/N)")
    if present == "Y" or present == "y":
      return True
    return False

  
# Test if testcase fails on buggy_js
output = Utils.run(info["failing_js"], info["original_test"])
if output == -1:
    exit("Couldn't run the buggy js parser")
output2 = Utils.run(info["js"], info["original_test"])
if output2 == -1:
    exit("Couldn't run normal js parser")

if not present(output, output2):
    exit("Bug isn't present anymore in original test")

# Format text in a better way
#print "Formatting JS testcase"
if os.path.exists(info["reduced_test"]):
    print "Already done"
else:
    f = open(info["original_test"], 'r')
    #data = "\r".join(f.readlines());
    data = "".join(f.readlines());
    f.close()

    f = open(info["reduced_test"], 'w')
#    f.write(jsbeautifier.beautify(data))
    f.write(data)
    f.close()
# TODO: change , of vars into ;
# TODO: change ()? : into if() {} else {} construction

# Test integrity reduced testcase
output = Utils.run(info["failing_js"], info["reduced_test"])
if output == -1:
    exit("Reduced testcase gives an error when run.")
output2 = Utils.run(info["js"], info["reduced_test"])
if output2 == -1:
    exit("Reduced testcase gives an error when run.")
if not present(output, output2):
    exit("Bug isn't present anymore in reduced testcase")

# Reduce
f = open(info["reduced_test"], 'r')
lines = len(f.readlines());
f.close()

script = Script(info)
reducer = Reducer(script)
#reducer.start()

#reducer.line(0, lines)

import random
while 1:
  length = random.randint(0, 100)+1
  line = random.randint(0, len(reducer.script.lines)-10)
  print line, line+length
  lines = reducer.script.lines
  reducer.line(line, line+length)


print lines,
f = open(info["reduced_test"], 'r')
lines = len(f.readlines());
f.close()
print "=>", lines

