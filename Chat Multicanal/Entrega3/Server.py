from socket import *
import sys
import threading

#Global Variables
clientList = []

class Client:
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
	group = 'default'

def broadcast(client,message):
	for i in range(len(clientList)):
		targetClient = clientList[i]
		if (client.socket != targetClient.socket):
			try: 	
				targetClient.socket.send(message)
			except:
				targetClient.socket.close()
				if targetClient in clientList:
					clientList.remove(targetClient)

def newClient(client):
	while True:
		#Receive text from the client
		sentence = client.socket.recv(2048)
		if not sentence: sys.exit(0)
		#command = sentence.split(' ',1)[0]
		values = ' Port '.join(str(v) for v in client.address)
		sentence= 'IP '+values+': '+sentence
		t=threading.Thread(target=broadcast, args=(client,sentence))
		t.daemon=True
		t.start()
		print sentence
	connectionSocket.close()

# Default port number server will listen on
serverPort = 12001

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

while True:
	# Wait for a client to connect to welcome port, establish
	# a new socket connection to the client on a transient port
	connectionSocket, addr = serverSocket.accept()
	client = Client(connectionSocket,addr)
	clientList.append(client)
	#Create a new thread with newClient
	t=threading.Thread(target=newClient, args=(client,))
	#If the main process dies, this thread dies too
	t.daemon=True
	#Starts the thread
	t.start()
# Close down the client's socket, not the welcome port
connectionSocket.close()
