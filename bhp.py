#netcat clone in python

import sys
import socket
import getopt
import threading
import subprocess

#global variables
listen = False
command = False
upload = False
execute = ""
target = ""
uploadDestination = "" 
port = 0

def usage():
    print "BHP CHAPTER 2 NET TOOL"
    print 
    print "Usage: bhpnet.py -t <target> -p <port>"
    print " -l listen"
    print " -e --execute=<filetorun>"
    print " -c --command"
    print " -u --upload=<destination>"
    
    sys.exit(0)
    
def main():
    global listen
    global port
    global execute
    global command
    global uploadDestination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", ["help", "listen", "execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            uploadDestination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"unhandled option"
            
        #if not listening, just sending data
        if not listen and len(target) and port > 0:
            buffer = sys.stdin.read()
            #read in command from commandline.
            client_sender(buffer)
            #send
            
        #if listen and potentially upload, execute and drop shell
        if listen:
            server_loop()
main()