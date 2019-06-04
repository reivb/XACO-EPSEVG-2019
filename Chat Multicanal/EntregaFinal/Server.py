#Sergio Santamaria - Xavi Diban - XACO 2019 UPC
from socket import *
import sys
import threading

#Global Variables
groupList = []
userList = []
CRED = '\033[91m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBEIGE  = '\33[36m'
CEND = '\033[0m'
#Classes (Data Structure)
class Client:
	def __init__(self, socket, address, group):
		self.socket = socket
		self.address = address
		self.group = group
		self.name = ''

class Group:
	def __init__(self, name):
		self.name = name
		self.users = []

#Broadcast function, sents message to all users in the same group channel as the Client
def broadcast(client,sentence,group):
		message = client.name+'('+group.name+')'+':'+sentence
		for i in range(len(group.users)):
			targetClient = group.users[i]
			#Sender doesn't receive his own message
			if (client.socket != targetClient.socket):
				try: 	
					targetClient.socket.send(CBEIGE+message+CEND)
				except:
					#If message can't be sent, targetClient is removed from the all his groups and closes his socket
					targetClient.socket.close()
					for group in groupList:						
						if targetClient in group.users:
							group.users.remove(targetClient)
					userList.remove(targetClient)

#If groupName exists in groupList, groupExistence returns true, false otherwise   
def groupExistence(groupName):
	groupExists = False
	i = 0
	while not groupExists and i<len(groupList):
		if groupList[i].name == groupName:
			groupExists = True
		else:
			i = i + 1
	return groupExists

def isUserInGroup(client,groupName):
	userInGroup = False
	for group in groupList:
		if group.name == groupName:
			for user in group.users:
				if user == client:
					userInGroup = True
	return userInGroup

def newClient(client):
	pickedUser = True
	client.socket.send(CYELLOW+'Introdueix el teu usuari'+CEND)
	#Loop until the given user is not taken
	while (pickedUser):
		pickedUser = False
		#Receive username from the client
		newClientName = client.socket.recv(2048)
		if not newClientName: sys.exit(0)
		for group in groupList:
			for user in group.users:
				if user.name == newClientName:
					pickedUser = True
					client.socket.send(CRED+'Usuari en us, introdueix un altre usuari'+CEND)
	client.name = newClientName
	client.socket.send(CGREEN+'El teu usuari es '+client.name+CEND)
	while True:
		#Receive text from the client
		sentence = client.socket.recv(2048)
		if not sentence: sys.exit(0)
		command = sentence.split(' ',1)[0]
		#New group command
		if command == 'CREA':
			try:
				#Command requires 2 arguments
				commandText = sentence.split()[1]
				correctCommand = True
			except:
				correctCommand = False
				client.socket.send(CRED+'Falta nom del canal'+CEND)
			if correctCommand:
				if not groupExistence(commandText):
					group = Group(commandText)
					groupList.append(group)
					client.socket.send(CGREEN+'Canal '+commandText+' creat'+CEND)
				else:
					client.socket.send(CRED+'El canal ja existeix'+CEND)
		elif command == 'UNIRSE':
			try: 
				#Command requires 2 arguments
				commandText = sentence.split()[1]
				correctCommand = True
			except:
				correctCommand = False
				client.socket.send(CRED+'Falta nom del canal'+CEND)
			if correctCommand:
				if not groupExistence(commandText):
					client.socket.send(CRED+'El canal no existeix'+CEND)
				elif isUserInGroup(client,commandText):
					client.socket.send(CRED+'Ja estas en el canal '+group.name+CEND)		
				else:
					for group in groupList:
						if group.name == commandText:
							group.users.append(client)	
							client.socket.send(CGREEN+'Te has unit al canal '+group.name+CEND)
		elif command == 'SORTIR':
			try: 
				#Command requires 2 arguments
				commandText = sentence.split()[1]
				correctCommand = True
			except:
				correctCommand = False
				client.socket.send(CRED+'Falta nom del canal'+CEND)
			if correctCommand:
				if not groupExistence(commandText):
					client.socket.send(CRED+'El canal no existeix'+CEND)
				elif not isUserInGroup(client,commandText):
					client.socket.send(CRED+'No pots sortir, no estabas en el canal '+group.name+CEND)		
				else:
					for group in groupList:
						if group.name == commandText:
							if group.name == client.group:
								client.socket.send(CRED+'No pots sortir del teu canal actiu. Canviat primer amb CANVIA "Canal"'+CEND)
							else:
								group.users.remove(client)
								client.socket.send(CGREEN+'Has sortit del canal '+commandText+CEND)
		elif command == 'CANVIA':
			try: 
				#Command requires 2 arguments
				commandText = sentence.split()[1]
				correctCommand = True
			except:
				correctCommand = False
				client.socket.send(CRED+'Falta nom del canal'+CEND)
			if correctCommand:
				if not groupExistence(commandText):
					client.socket.send(CRED+'El canal no existeix')
				elif not isUserInGroup(client,commandText):
					client.socket.send(CRED+'No estas en el canal '+commandText+'. Afegeix-te amb UNIRSE "Canal"'+CEND)
				elif client.group == commandText:
					client.socket.send(CRED+commandText+' ja es el teu canal actual'+CEND)		
				else:
					client.socket.send(CGREEN+'El teu nou canal de emissio es '+commandText+CEND)
					client.group = commandText

		#Show groups command
		elif command == 'MOSTRA_CANALS':
			message = 'Canals: '			
			for group in groupList:
				message += ''.join(str(v) for v in group.name)+' '
			client.socket.send(CYELLOW+message+CEND)
		elif command == 'MOSTRA_CANALS_USUARI':
			message = 'Canals del usuari: '			
			for group in groupList:
				for user in group.users:
					if user == client:
						message += ''.join(str(v) for v in group.name)+' '
			client.socket.send(CYELLOW+message+CEND)
		#Show users in current client.group
		elif command == 'MOSTRA_USUARIS':
			message = 'Usuaris: '	
			for group in groupList:
				if group.name == client.group:
					for user in group.users:
						message += ''.join(str(v) for v in user.name)+' '
			client.socket.send(CYELLOW+message+CEND)
		#Show users in server
		elif command == 'MOSTRA_TOTS':
			message = 'Usuaris: '
			for user in userList:
				message += ''.join(str(v) for v in user.name)+' '
			client.socket.send(CYELLOW+message+CEND)
		elif command == 'ACTUAL':
			client.socket.send(CYELLOW+'Emets per el canal '+client.group+CEND)
		#Private message command
		elif command == 'PRIVAT':
			try: 
				#Command requires 3 arguments
				commandText = sentence.split()[1]
				text = sentence.split(' ', 2)[2]
				correctCommand = True
			except:
				correctCommand = False
				client.socket.send(CRED+'Faltan arguments'+CEND)
			if correctCommand:
				messageSent = False
				for group in groupList:
					if group.name == client.group:
						for user in group.users:
							if user.name == commandText:
								values = ''.join(str(v) for v in client.name)
								message = 'Privat de '+values+':'+text
								user.socket.send(CBEIGE+message+CEND)
								messageSent = True
				if not messageSent:
					client.socket.send(CRED+'El usuari no es troba en el mateix canal'+CEND)
		elif command == 'DIFONDRE':
			text = sentence.split(' ', 1)[1]
			for group in groupList:
				if client in group.users:
					broadcast(client,text,group)	
		elif command == 'HELP':

			client.socket.send(CYELLOW+'ACTUAL\nCANVIA "Canal"\nCREA "Canal"\nDIFONDRE\nMOSTRA_CANALS\nMOSTRA_CANALS_USUARI\nMOSTRA_TOTS\nMOSTRA_USUARIS\nPRIVAT "Usuari" "Missatge"\nSORTIR\nUNIRSE "Canal"'+CEND)
		else:
			values = ' Port '.join(str(v) for v in client.address)
			serverSentence = 'IP '+values+' '+client.group+' '+client.name+':'+sentence
			print serverSentence
			#Searches the Group of the client group
			for group in groupList:
				if group.name == client.group:
					targetGroup = group
			#Create a new thread with newClient
			t=threading.Thread(target=broadcast, args=(client,sentence,targetGroup))
			#If the main process dies, this thread dies too			
			t.daemon=True
			#Starts the thread
			t.start()
	# Close down the client's socket, not the welcome port
	connectionSocket.close()

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
group = Group('default')
groupList.append(group)
while True:
	# Wait for a client to connect to welcome port, establish
	# a new socket connection to the client on a transient port
	connectionSocket, addr = serverSocket.accept()
	client = Client(connectionSocket,addr,group.name)
	for group in groupList:
		if group.name == 'default':
			group.users.append(client)
	userList.append(client)
	#Create a new thread with newClient
	t=threading.Thread(target=newClient, args=(client,))
	#If the main process dies, this thread dies too
	t.daemon=True
	#Starts the thread
	t.start()
# Close down the client's socket, not the welcome port
connectionSocket.close()
