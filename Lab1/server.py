#!/usr/bin/python           # This is client.py file
import socket


# Before run multithread! Learn how to kill it first!
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.bind((socket.gethostname(), 80))
serversocket.bind(('localhost', 3000))
serversocket.listen(5)
# fileName = './TestFile.txt'
fileName = './Boston.mp3'
while True:
	try:
		(clientsocket, address) = serversocket.accept()
		# ct = client_thread(clientsocket)
		# ct.run()
		print("Client is ", address)
		f = open(fileName, "r")
		l = f.read(1024)
		while l:
			clientsocket.send(l)
			l = f.read(1024)
		clientsocket.close()
		f.close()
	except KeyboardInterrupt:
		print 'Exiting program'
		break