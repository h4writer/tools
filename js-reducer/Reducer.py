import signal
import subprocess
import os
import re

class Utils:

    @staticmethod
    def cp(input_test, output_test):
        cmd = "cp "+input_test+" "+output_test
        proc = subprocess.Popen(  cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        output, error = proc.communicate('through stdin to stdout')
        assert len(error) == 0

    @staticmethod
    def fileRemoveLines(input_test, output_test, start, end):
        cmd = "sed '"+str(start+1)+","+str(end)+"d' "+input_test+" > "+output_test
        proc = subprocess.Popen(  cmd, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        output, error = proc.communicate('through stdin to stdout')
        assert len(error) == 0

    @staticmethod
    def run(js, testfile):
        if "%s" in js:
          cmd = js.replace("%s", testfile)
        else:
          cmd = js+" "+testfile

        class TimeException(Exception):
            pass

        def timeout_handler(signum, frame):
            raise TimeException()

        signal.signal(signal.SIGALRM, timeout_handler) 
        signal.alarm(2) # triger alarm in 3 seconds

        try:
            proc = subprocess.Popen(  cmd, shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            output, error = proc.communicate('through stdin to stdout')
            signal.alarm(0)
            return error+output
        except TimeException:
            #os.kill(proc.pid+1, signal.SIGINT) # no idea why + 1, but the reported pid isn't right ?!
            subprocess.Popen("killall js", shell=True)
            return -1

    @staticmethod
    def verify(output, verification):

        """try:
          return int(output) > 50
        except:
          return False;"""
        """return "31\n" in output or "26\n" in output"""

        return verification in output

    @staticmethod
    def test(buggy_js, js, tmp, verification):
        output = Utils.run(buggy_js, tmp)
        if output == -1 or not Utils.verify(output, verification):
            return False

        output = Utils.run(js, tmp)
        if output == -1 or Utils.verify(output, verification):
            return False;

        return True

    @staticmethod
    def numeric(output):
      m = re.search( r'([0-9]+(\.[0-9]+)+)', output)
      return float(m.group(0))

class Script:

    def __init__(self, info):
        self.info = info

        f = open(info["reduced_test"], 'r')
        self.lines = f.readlines()
        self.tmplines = self.lines[:]
        f.close()

    def removeLines(self, start, end):
        #print start, "-", end
        self.tmplines = self.lines[:start] + self.lines[end:]
        Utils.fileRemoveLines(self.info["reduced_test"], self.info["temp_test"], start, end)

    def test(self):
        if Utils.test(self.info["failing_js"], self.info["js"], self.info["temp_test"], self.info["verification"]):
            Utils.cp(self.info["temp_test"], self.info["reduced_test"])
            self.lines = self.tmplines[:]
            return True
        return False

    def isStatement(self, lineno, depth=0):
        line = self.lines[lineno]
        if line[:4*(depth+1)] == "    "*(depth+1):
            return False
        elif "{" in line or "}" in line:
            return False

        return True 

    def isBlockStart(self, lineno, depth=0):
        line = self.lines[lineno]
        if line[:4*(depth+1)] == "    "*(depth+1):
            return False
        elif "{" in line:
            return True
        return False

    def isBlockEnd(self, lineno, depth=0):
        line = self.lines[lineno]
        if line[:4*(depth+1)] == "    "*(depth+1):
            return False
        elif "}" in line:
            return True
        return False

class Reducer:

    def __init__(self, script):
        self.script = script

    def start(self):

        end = len(self.script.lines)
        self.statements(0, end)

    def statements(self, start, end, depth=0):
        print "statements", start, end

        end -= 1
        while end > start:
            if self.script.isStatement(end, depth):
                # find longest list of statements
                i = end-1
                while self.script.isStatement(i, depth) and i >= start:
                    i -= 1
                self.line(i+1, end+1)
                end = i+1

            elif self.script.isBlockEnd(end, depth):
                # find block start
                i = end-1
                while not self.script.isBlockStart(i, depth) and i >= start:
                    i -= 1

                if self.script.isBlockStart(i, depth):
                    self.block(i, end+1, depth)
                    end = i

            end -= 1

    def block(self, start, end, depth=0):
        # try removing total block
        self.script.removeLines(start, end)
        if self.script.test():
            return

        # remove statements in block
        self.statements(start+1, end-1, depth+1)

        # TODO: if function inline


    def line(self, start, end = -1):
        """
        Tries to remove lines between start and end
        """
        if end == -1:
            end = start
            start = 0
        elif start > end:
            end, start = start, end

        remove_start = start
        while 1:
            #print len(self.script.lines)

            self.script.removeLines(remove_start, end)
            if self.script.test():
                print len(self.script.lines)
                #print remove_start,"-",end, "remove"
                end -= end - remove_start
                remove_start = start
                if end == start:
                    return
            else:
                if (end - remove_start)/2 != 0:
                    remove_start += (end - remove_start)/2
                else:
                    remove_start = start
                    end -= 1
                    if end == remove_start:
                        return

    def line1(self, start, end = -1):
        self.script.removeLines(start, end)
        self.script.test()
