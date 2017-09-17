#!/usr/bin/python

import socket,sys

DEFAULT_HTTP_VERSION = 'HTTP/1.0'
DEFAULT_BUFFER_SIZE = 1024
DEFAULT_DOWNLOAD_FOLDER = './Download'

def main(args):
	# Parse input
	host = args[0]
	port = int(args[1])
	filePath = args[2]
	request_method = args[3]

	# Convert '/' to /index.html
	if filePath == '/':
		filePath = '/index.html'

	# Setup the download path
	localFileName = DEFAULT_DOWNLOAD_FOLDER + filePath[filePath.rfind('/'):]

	# Build a simple request
	request = "{0} {1} {2}\n".format(request_method, filePath, DEFAULT_HTTP_VERSION)  
	
	# Create a socket, and send the requests
	s = socket.socket()
	s.connect((host, port))
	s.sendall(request)

	# prepare the file to write
	f = open(localFileName, "w")

	# Buffer the responce
	l = s.recv(DEFAULT_BUFFER_SIZE)

	# Check the responce status
	responce = l.splitlines()[0]
	responce = responce.strip()
	status = responce.split()[1]

	# If get request, only retrive the body
	if request_method == 'GET' and status == '200':
		# Looking for the starting symbol of the body
		body_start = l.find('\r\n\n')
		# If have not seen body, keep reading until seen
		haveSeenBody = False
		
		while l:
			# If have seen the body tag, the input has to be body, just write to file
			if haveSeenBody:
				f.write(l)
			# If have not read body yet, but found the body starting tag
			elif not haveSeenBody and body_start != -1:
				# find the starting of the responce body
				l = l[body_start:].lstrip()
				f.write(l)
				haveSeenBody = True

			l = s.recv(DEFAULT_BUFFER_SIZE)
			body_start = l.find('\r\n\n')
	# If HEAD request, retrive everything

	else:
		# Write to file until the socket is empty
		print l
		while l:
			f.write(l)
			l = s.recv(DEFAULT_BUFFER_SIZE)

	# Close socket
	s.close()
	# Close file
	f.close()

if __name__ =='__main__':
	args = sys.argv[1:]
	# Assume only 4 inputs are allowed, they are host, port, file_path, and GET/HEAD method
	if not len(args) == 4:
		print "Cannot understand the request~"

	try:
		main(args)
	except Exception:
		print "Your input has problems!"



