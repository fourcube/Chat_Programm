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

DEBUG=False
USERNAME=""

def prompt() :
    sys.stdout.write('<%s> ' % USERNAME)
    sys.stdout.flush()

def receive_message(data):
    packet_type = protocol.get_type(data)

    if packet_type is protocol.PING:
        if DEBUG:
            print("\nDEBUG: PING")
            prompt()
        return
    elif packet_type is protocol.TEXT:
        decryptedData = decryptedMessage(data, 6)
        unpacked = protocol.unpack_text(decryptedData)
        sys.stdout.write('\r' + unpacked + '\n')
    elif packet_type is protocol.CLIENT_MESSAGE:
        decryptedData = decryptedMessage(data, 6)
        unpacked = protocol.unpack_client_message(decryptedData)
        sys.stdout.write("\r<%s> %s" % (unpacked[0], unpacked[1]))

    prompt()

#main function
if __name__ == "__main__":

    if(len(sys.argv) < 3) :
        print 'python chat_server.py ip port username <debug>'
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    USERNAME = sys.argv[3]
    if len(sys.argv) > 4:
        DEBUG = True
        print "Debug mode active."

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

            #user entered a message
            else:
                msg = sys.stdin.readline()
                packed = protocol.pack_client_message(USERNAME, msg)
    	        encryptedData = encryptedMessage(packed, 6)
                s.send(encryptedData)
                prompt()
