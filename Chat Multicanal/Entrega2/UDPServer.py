# Simple UDP based server that upper cases text
import sys
from socket import *

# Default to listening on port 12000
serverPort = 12000

# Optional server port number
if (len(sys.argv) > 1):
	serverPort = int(sys.argv[1])

# Setup IPv4 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Specify the welcoming port of the server
serverSocket.bind(('', serverPort))

print "The server is ready to receive"
while 1:
	# Wait for a client to arrive, returns a new socket associated with the client
	message, clientAddress = serverSocket.recvfrom(2048)

        print message
        sentence2 = raw_input('Answer:')
	# Sent the converted text back to whoever sent us the message
	serverSocket.sendto(sentence2, clientAddress)
serverSocket.close()
