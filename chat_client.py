#! /usr/bin/env python
# coding: utf-8
#
# Chat Client
#
#
# author: gnivciv
# last edit: 18.01-2015
# original source: http://www.binarytides.com/code-chat-application-server-client-sockets-python/
#

import socket, select, string, sys

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def encryptedMessage(message, key):
	encrypted = ''
	for symbol in message:
        	if symbol.isalpha():
        	    num = ord(symbol)
        	    num += key
        	    if symbol.isupper():
        	        if num > ord('Z'):
        	            num -= 26
        	        elif num < ord('A'):
        	            num += 26
        	    elif symbol.islower():
        	        if num > ord('z'):
        	            num -= 26
        	        elif num < ord('a'):
        	            num += 26
        	    encrypted += chr(num)
        	else:
        	    encrypted += symbol	
		global msg		
		msg = encrypted	

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'python chat_server.py ip port'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Keine Verbindung zum Server'
        sys.exit()

    print 'Verbunden mit Server. Beginne Nachrichten zu schreiben.'
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nVom Server getrennt'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt()

            #user entered a message
            else :
                msg = sys.stdin.readline()
		encryptedMessage(msg, 6)
		s.send(msg)
                prompt()
