#!/usr/bin/python           # This is client.py file

import socket,sys 
DEFAULT_HTTP_VERSION = 'HTTP/1.0'
def main(args):
	s = socket.socket()       
	host = args[0]  		
	port = int(args[1])

	filePath = args[2]
	request_method = args[3]
	# host = 'localhost'  		
	# port = 3000
	# filePath = '/'
	# request_method = 'GET'



	if filePath == '/':
		filePath = '/index.html'

	localFileName = './Download' + filePath[filePath.rfind('/'):]
	request = "{0} {1} {2}".format(request_method, filePath, DEFAULT_HTTP_VERSION)
	
	s.connect((host, port))
	s.sendall(request)

	f = open(localFileName, "w")
	l = s.recv(1024)

	if request_method == 'GET':
		body_start = l.find('\r\n\n')
		haveSeenBody = False
		while l:
			if haveSeenBody:
				f.write(l)
			elif not haveSeenBody and body_start != -1:
				l = l[body_start:].lstrip()
				f.write(l)
				haveSeenBody = True
			l = s.recv(1024)
	else:
		while l:
			f.write(l)
			l = s.recv(1024)

	s.close()
	f.close()

if __name__ =='__main__':
	args = sys.argv[1:]
	if not len(args) == 4:
		print "Cannot understand the request~"

	try:
		main(args)
	except Exception:
		print "Your input has problems!"