#!/usr/bin/env python

import socket
import os

def simpleClient():

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.connect(("www.google.com", 80))

	clientSocket.sendall("GET / HTTP/1.0\r\n\r\n")

	while True:
		part = clientSocket.recv(1024)
		if len(part)>0:
			print part
		else:
			exit(0)
	

def simpleProxy():
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.bind(("0.0.0.0", 8080))
	clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
	clientSocket.listen(5)

	while True:

		(incommingSocket, address) = clientSocket.accept()
		print "we got a connection from %s!" % (str (address))
		pid = os.fork()
		if (pid == 0):

			googleSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	
			# googleSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
			googleSocket.connect(("www.google.com", 80))
			incommingSocket.setblocking(0)
			googleSocket.setblocking(0)

			while True:
				#This half forwads from client to google
				skip = False
				try:
					part = incommingSocket.recv(1024)
				except socket.error, exception:
					if exception.errno == 11:
						skip=True
					else:
						raise

				if not skip:		
					if len(part) > 0 :
						print " > " + part
						googleSocket.sendall(part)
					else:
						exit(0)

				#This half forwards from google to client
				skip = False
				try:
					part = googleSocket.recv(1024)
				except socket.error, exception:
					if exception.errno == 11:
						skip=True
					else:
						raise

				if not skip:		
					if (len(part)) > 0:
						print " < " + part
						incommingSocket.sendall(part)
					else:
						exit(0)


if __name__=="__main__":
	# simpleProxy()
	simpleClient()