#!/usr/bin/python           # This is client.py file
import socket, sys, time

DEFAULT_BUFFER_SIZE = 1024
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = '3000'
DEFAULT_CONNECTIONS = 5
DEFAULT_FILE_LOCATIONS = './Upload'

def main(port):
	# Before run multithread! Learn how to kill it first!
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.bind((DEFAULT_HOST, port))
	serversocket.listen(DEFAULT_CONNECTIONS)

	while True:
		try:
			(cSocket, address) = serversocket.accept()
			# ct = client_thread(cSocket)
			# ct.run()

			print("Client is ", address)

			parseRequest(cSocket)
			# dummyRespond(cSocket)

			# requestType, requestBody = parseRequest(cSocket)

			# if requestType == 'GET':
			# 	handleGetRequest(requestBody)
			# elif requestType == 'HEAD':
			# 	handleHeadRequest(requestBody)
			# else:
			# 	handleBadRequest()

			cSocket.close()
			print "finsihed process"
		except KeyboardInterrupt:
			print 'Bye bye!\n'
			sys.exit()

def dummyRespond(cSocket):
	f = open('./HTTP_Reply_messages/200.html', "r")
	l = f.read(1024)
	while l:
		cSocket.send(l)
		l = f.read(1024)
	f.close()
	print "done sending file!"
	pass

def parseRequest(cSocket):
	temp = cSocket.recv(DEFAULT_BUFFER_SIZE)
	# raw_request = "temp[:]\n adas"
	while temp:
		print temp
		print "I am before read"
		dummyRespond(cSocket)
		# time.sleep(1)
		cSocket.settimeout(5.0) 
		temp = cSocket.recv(DEFAULT_BUFFER_SIZE)
		print "I am after read"
		temp = None
		# raw_request+=temp[:]
	# print raw_request.split('\n')[0]
	print "I am here"
	# dummyRespond(cSocket)
	pass

def handleGetRequest():
	pass

def handleHeadRequest():
	pass

def handleBadRequest():
	pass

if __name__ =='__main__':
	# main(sys.argv[1:])
	args = sys.argv[1:]
	if not len(args) == 1 or not args[0].isdigit():
		print 'Command not supported. \nExample: python server.py 1234\n'
		sys.exit()
	main(int(args[0]))




