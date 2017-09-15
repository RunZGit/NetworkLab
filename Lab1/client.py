#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = 'localhost'  		# Get local machine name
port = 3000                	# Reserve a port for your service.

s.connect((host, port))

file = './ClientDownload/Boston.mp3'
f = open(file, "w")
l = s.recv(1024)
while l:
	f.write(l)
	l = s.recv(1024)

s.close()
f.close()              