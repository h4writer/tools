#!/usr/local/bin/python

import socket
import ssl
import time
import re
import threading
import os

## Settings
### IRC
server = "irc.mozilla.org"
port = 6667
channel = "#h4writer"
botnick = re.sub(r'[^a-zA-Z0-9: ]', '', socket.gethostname())
alert_file = '/tmp/alert'

##

class WorkerThread(threading.Thread):
    stop_ = False

    def stop(self):
        self.stop_ = True
    def run(self):
        tail_line = 0

        while not self.stop_:
            time.sleep(2)
            # Tail Files
            if os.path.exists(alert_file):
                f = open(alert_file, 'r')
                lines = f.readlines()
                f.close()
                if tail_line != len(lines):
                    tail_line = len(lines)
                    irc.send("PRIVMSG %s :h4writer: %s" % (channel, lines[-1]))

if __name__ == '__main__':
    worker = WorkerThread()

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket

    print "Establishing connection to [%s]" % (server)
    irc.connect((server, port))
    print irc.recv ( 4096 )
    irc.send("NICK "+ botnick +"\n")
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :meLon-Test\n")

    try:
        while True:
            data = irc.recv ( 4096 )
            #print data

            if data.find ( 'Welcome to the Mozilla IRC Network' ) != -1:
                irc.send ( 'JOIN ' + channel + '\r\n' )

                worker.start()

            if data.find ( 'PING' ) != -1:
                irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    finally:
        worker.stop()
