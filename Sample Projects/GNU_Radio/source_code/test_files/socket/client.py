#!/usr/bin/env python
# Echo client program
import socket
import sys

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#print 'Connected to', s.getpeername()
#while 1:
#    action = int(raw_input('Enter your action, 1=wait, 0=send: '))
#    if not action:
       #time.sleep(5)
    #else:
#        break
raw_input('ready to send?: ')
fpR = open('/root/Desktop/CC_ver1.0.0.1/Sender/JpegEncoder/Output.jpg', 'r')
data=fpR.read(-1)
sent=s.send(data)
print "total sent ", sent, "bytes"
print "send finished"

while 1:
	action=int(raw_input('send again?: 1=yes, 0=no'))
	if not action:
		break
	sent=s.send(data)
	print "total sent ", sent, "bytes"
	print "send finished"
"""
# read echo
i = 0
t=0
while(1):
    data = s.recv(1000) # read up to 1000000 bytes
    i += 1
    if (i < 5):
        print data
    if not data: # if end of data, leave loop
        break
    t=t+len(data)
    print 'received', len(data), 'bytes'

print 'total received', t, 'bytes'

"""
#s.send('finished')
z=raw_input('close client?: ')
s.close()
#while 1:
sent=s.send('james')
print "total sent ", sent, "bytes"
#s.close()
#print 'Received', repr(data)
