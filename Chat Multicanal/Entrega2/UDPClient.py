# Example UDP socket client that fires some text at a server
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
        # Request IPv4 and UDP communication
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # Read in some text from the user
        message = raw_input('Input:')

        # Send the text and then wait for a response 
        clientSocket.sendto(message, (serverName, serverPort))

        message2, serverAddress = clientSocket.recvfrom(2048)

        # Print the converted text and then close the socket
        #message2 = clientSocket.recvfrom(2048)
        print 'From Server:', message2
clientSocket.close()
