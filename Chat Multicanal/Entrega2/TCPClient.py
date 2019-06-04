# Example TCP socket client that connects to a server that upper cases text
import sys
from socket import *

# Default to running on localhost, port 12000
serverName = 'localhost'
serverPort = 12000

# Optional server name argument
if (len(sys.argv) > 1):
	serverName = sys.argv[1]

# Optional server port number
if (len(sys.argv) > 2):
	serverPort = int(sys.argv[2])
while 1:
        # Request IPv4 and TCP communication
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Open the TCP connection to the server at the specified port 
        clientSocket.connect((serverName,serverPort))



        # Read in some text from the user
        sentence = raw_input('Input:')
        #capitalizedSentence = sentence.upper()
        # Send the text and then wait for a response 
        clientSocket.send(sentence)
        serverSentence = clientSocket.recv(2048)
        # Print the converted text and then close the socket
        print 'From Server:', serverSentence
        clientSocket.close()
