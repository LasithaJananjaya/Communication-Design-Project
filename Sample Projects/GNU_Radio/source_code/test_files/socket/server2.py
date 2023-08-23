#!/usr/bin/env python
# Echo server program
import socket
import sys

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
print 'after listen'
conn, addr = s.accept()
print 'socket_ID is',conn
print 'socket for listen is', s.getsockname()
print 'server port of accept is',conn.getsockname()
print 'Connected by', addr
i=0
action=1
while action:
	i=i+1
	print 'this is the ', i, 'time recieve'
	while 1:
   		data = conn.recv(1000)

		print 'receive data: ', repr(data)
		print 'len of data= ', len(data)
		if not data:
			break
	print 'finish'
	action=int(raw_input('continue receive?: 1=continue, 0=stop'))
raw_input('begin server send?: ')
conn.send('james')
#if not data:
raw_input('close server?: ')
conn.close()


#while (1):
#    data=conn.recv(1000)
#    print data
#    if not data:
#        break
#print 'get /0'
