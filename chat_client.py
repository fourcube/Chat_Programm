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

import socket
import select
import string
import sys
import protocol

from crypto import encryptedMessage, decryptedMessage

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()

def receive_message(data):
    packet_type = protocol.get_type(data)
    if packet_type is protocol.PING:
        print("PING")
    elif packet_type is protocol.TEXT:
        decryptedData = decryptedMessage(protocol.unpack_text(data), 6)
        sys.stdout.write(decryptedData)

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
        print "Can't connect to server"
        sys.exit()

    print 'Connected to server. Start to write messages.'
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
                    print '\nDisconnected from server'
                    sys.exit()
                else:
                    #print data
                    receive_message(data)

                prompt()

            #user entered a message
            else:
                msg = sys.stdin.readline()
	        encryptedData = encryptedMessage(msg, 6)
	        s.send(protocol.pack_text(encryptedData))
                prompt()
