# TCP server program that upper cases text sent from the client
from socket import *
import sys
import threading

# Default port number server will listen on
serverPort = 12000

# Optional server port number
if (len(sys.argv) > 1):
	serverPort = int(sys.argv[1])

# Request IPv4 and TCP communication
serverSocket = socket(AF_INET,SOCK_STREAM)

# The welcoming port that clients first use to connect
serverSocket.bind(('',serverPort))

# Start listening on the welcoming port
serverSocket.listen(1)
print 'The server is ready to receive'
while 1:

	# Wait for a client to connect to welcome port, establish
     	# a new socket connection to the client on a transient port
     	connectionSocket, addr = serverSocket.accept()
     
	# Get the text the client wants us to work on
	sentence = connectionSocket.recv(2048)
	#Print the recieved sentence
	print sentence
        
        #Read the answer
	sentence2 = raw_input('Answer: ')
	#capitalizedSentence = sentence2.upper()
	

	# Send back the converted text to the client
	connectionSocket.send(sentence2)

# Close down the client's socket, not the welcome port
connectionSocket.close()

