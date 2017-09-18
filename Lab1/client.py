#!/usr/bin/python

import socket,sys

DEFAULT_HTTP_VERSION = 'HTTP/1.0'
DEFAULT_BUFFER_SIZE = 1024
DEFAULT_LARGE_BUFFER_TRHESHOLD = 1024 * 100
DEFAULT_DOWNLOAD_FOLDER = './Download'

def main(args):
	# Parse input
	host = args[0]
	port = int(args[1])
	filePath = args[2]
	request_method = args[3]
	verbose = False
	if len(args) == 5:
		verbose = bool(args[4] == 'True')

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

	# Buffer the responce
	l = s.recv(DEFAULT_BUFFER_SIZE)

	# Check the responce status
	responce = l.splitlines()[0]
	responce = responce.strip()
	status = responce.split()[1]

	# Only responce 200 has response body, else we can just print the meta
	if status == '302' and request_method == 'HEAD':

		fileExtesionIndex = filePath.rfind('.')
		# if fileExtesionIndex == -1:
		# 	fileExtesionIndex = len(filePath)

		localFileName = DEFAULT_DOWNLOAD_FOLDER+filePath[filePath.rfind('/'):fileExtesionIndex]+'_HEAD'
		# +filePath[fileExtesionIndex:]
		
		f = open(localFileName, "w")
		while l:
			print l
			f.write(l)
			l = s.recv(DEFAULT_BUFFER_SIZE)
		f.close()

	elif status != '200':
		while l:
			print l
			l = s.recv(DEFAULT_BUFFER_SIZE)
	#If it is 200 response
	else:
	# Extract meta data:
		meta = ''
		end_of_meta = l.find('\r\n\n')

		#Append meta until we have seen the body
		while l and end_of_meta == -1:
			meta+=l
			l = s.recv(DEFAULT_BUFFER_SIZE)
			end_of_meta = l.find('\r\n\n')
		if end_of_meta == -1:
			print meta + '\n\r'
		#Found body
		if end_of_meta != -1:
			#Append the rest of the meta
			meta += l[:end_of_meta]
			#Convert the l to body
			print meta + '\n\r'
			
			#Prepare buffer
			total_length = 0
			lengthKeyword= 'Content-Length:'
			buffer_size = DEFAULT_BUFFER_SIZE

			for line in meta.splitlines():
				if line.startswith(lengthKeyword):
					total_length = int(line[(line.find(lengthKeyword)+len(lengthKeyword)):])
					break

			#Control the max buffer
			if total_length > DEFAULT_LARGE_BUFFER_TRHESHOLD:
				buffer_size = min(max(total_length/20, DEFAULT_BUFFER_SIZE), DEFAULT_LARGE_BUFFER_TRHESHOLD)

			l = l[end_of_meta:].lstrip()
			read_bytes = len(l)
			#Seen body, now write to file
			f = open(localFileName, "w")
			while l:
				f.write(l)
				if verbose:
					output = 'Progress: {0}/{1} '.format(str(read_bytes), str(int(total_length)))
					sys.stdout.write('\r'+output)

				l = s.recv(min(buffer_size, max(total_length-read_bytes, DEFAULT_BUFFER_SIZE)))
				read_bytes += len(l)
			#close the file
			f.close()
			if verbose:
				print '\n\r'

	# Close socket
	s.close()


if __name__ =='__main__':
	args = sys.argv[1:]
	# Assume only 4 inputs are allowed, they are host, port, file_path, and GET/HEAD method
	if not (len(args) == 4 or len(args) == 5): 
		print "Cannot understand the request~"
	# main(args)
	try:
		main(args)
	except Exception:
		print "Your input has problems! Please reference README"



