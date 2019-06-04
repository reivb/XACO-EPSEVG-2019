from socket import *
import sys
import threading

# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000

# Optional server name argument
if (len(sys.argv) > 1):
	serverName = sys.argv[1]

# Optional server port number
if (len(sys.argv) > 2):
	serverPort = int(sys.argv[2])

# Request IPv4 and TCP communication
clientSocket = socket(AF_INET, SOCK_STREAM)

# Open the TCP connection to the server at the specified port 
clientSocket.connect((serverName,serverPort))
print 'Connectat al servidor'
print 'IP:'+serverName+' Port:',serverPort

#Receive function
def recv():
	while True:
		#Receive text from the server
		sentence = clientSocket.recv(2048)
		if not sentence: sys.exit(0)
		#Prints the text sentence
		print sentence

#Create a new thread with recv function
t=threading.Thread(target=recv)
#If the main process dies, this thread dies too
t.daemon=True
#Starts the thread
t.start()

while 1:
	# Read in some text from the user
	sentence2 = raw_input()
	print 'Tu:',sentence2
	# Send the text
	clientSocket.send(sentence2)
	
clientSocket.close()
