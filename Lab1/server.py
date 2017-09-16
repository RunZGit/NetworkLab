#!/usr/bin/python           # This is client.py file
import socket, sys, time, os.path

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
			requestType, filePath = parseRequest(cSocket)
			handleRequest(cSocket, requestType, filePath)
			cSocket.close()
		except KeyboardInterrupt:
			print '\rBye bye!\n'
			serversocket.close()
			sys.exit()

def handleRequest(cSocket, requestType, filePath):
	if requestType == 'GET':
		handleGetRequest(cSocket,filePath)
	# elif requestType == 'HEAD':
	# 	handleHeadRequest(requestBody)
	# else:
	# 	handleBadRequest(requestBody)

def parseRequest(cSocket):
	request = cSocket.recv(DEFAULT_BUFFER_SIZE)
	request = request.split()
	requestType = request[0]
	filePath = request[1]
	return (requestType, filePath)

def handleGetRequest(cSocket, path):
	if path == "/":
		path = "/index.html"

	path = DEFAULT_FILE_LOCATIONS+path
	print "Looking for file: " + path
	content = loadFile(path)
	if not content:
		print "404 Not Found"
		http_response = "HTTP/1.0 404 Not Found \r\n\n"
	else:
		print "200 OK"
		http_response = "HTTP/1.0 200 OK \r\n"

		if path.endswith(".html"):
			http_response+= "Content-Type: text/html\r\n"
		elif path.endswith(".jpg"):
			http_response+= "Content-Type: image/gif\r\n"
		http_response += 'Last-Modified: ' + time.ctime(os.path.getmtime(path)) + '\r\n'
		http_response += 'Content-Length: ' + str(len(content)) +'\r\n\n'
		http_response+=content

	cSocket.sendall(http_response)

def handleHeadRequest():
	pass

def handleBadRequest(cSocket):

	pass

def loadFile(filePath):
	if os.path.exists(filePath):
		with open(filePath, 'r') as f:
			content = f.read()
		return content
	return False

if __name__ =='__main__':
	args = sys.argv[1:]
	if not len(args) == 1 or not args[0].isdigit():
		print 'Command not supported. \nExample: python server.py 1234\n'
		sys.exit()
	main(int(args[0]))




