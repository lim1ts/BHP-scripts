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
	#help message for -h and improper arguments	
    print ("BHP CHAPTER 2 NET TOOL")
    print 
    print ("Usage: bhpnet.py -t <target> -p <port>")
    print (" -l listen")
    print (" -e --execute=<filetorun>")
    print (" -c --command")
    print (" -u --upload=<destination>")
    
    sys.exit(0)

def client_sender(buffer):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	try:
		#connect to target host
		client.connect((target, port))	#target and port defined in main() as global variables.
		if len(buffer):
			client.send(buffer) #send write buffer data if exists.

		while True:
			#wait to receive data
			recv_len = 1
			response = ""
			
			while recv_len:
				# receives 4096b data each time, adds to response
				data = client.recv(4096)
				recv_len = len(data)
				response += data

				if recv_len < 4096:
					break
			print (response,)

			buffer = raw_input("")
			buffer += "\n" #extra line break is added since reading in raw input does not contain \n.
			client.send(buffer)

	except:
		print ("[*] Exception! Exiting")
		client.close()

def server_loop():
	global target

	if not len(target):
		target = "0.0.0.0"
	
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)

	while True:
		client_socket, addr = server.accept()
		client_thread = threading.Thread(target=client_handler, args =(client_socket,))
		client_thread.start()
    
def run_command(command):
	command = command.rstrip()
	try:
		output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
	except:
		output = "Failed to execute command. \r\n"

	return output


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
	#begin by reading all the options
    except getopt.GetoptError as err:
        print ("%s") % str(err)
        usage()
        #Simple parser for the options
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
	    #Will block - crtl-d if planning to send interactively
            client_sender(buffer)
            #send
            
        #if listen and potentially upload, execute and drop shell
        if listen:
            server_loop()
main()
