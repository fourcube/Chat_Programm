#! /usr/bin/env  python
# coding: utf-8
#
# Chat Server
#
#
# author: gnivciv
# version: 1.0
# last edit: 18.01.2015
# original source: http://www.binarytides.com/code-chat-application-server-client-sockets-python/
#

import socket
import select
import time
import sys

#Sendet Daten an ale Nutzer
def broadcast_data (sock_id, message):
    #Do not send the message to master socket and the client who has send us the message
    for id, socket in CONNECTION_LIST.items():
        if id != server_socket.fileno() and id != sock_id:
            try :
                socket.send(message)
            except Exception as e:
                #broadcast_data(id, "Client {} is offline.\n".format(id))
                del CONNECTION_LIST[id]

if __name__ == "__main__":

    if(len(sys.argv) < 2) :
        print 'python chat_server.py port'
        sys.exit()

    PORT = int(sys.argv[1])
    CONNECTION_LIST = {}
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
    server_sock_id = server_socket.fileno()

    # Add server socket to the list of readable connections
    CONNECTION_LIST[server_sock_id] = server_socket

    print "Server wurde gestartet, Port: " + str(PORT)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST.keys(),[],[])

        for sock_id in read_sockets:
            sock = CONNECTION_LIST.get(sock_id, None)
            if sock is None:
                continue

            #Neue Verbindung
            if sock_id == server_sock_id:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                id = sockfd.fileno()

                CONNECTION_LIST[id] = sockfd
                #print "{} Client {} connected".format(id, addr)
                #broadcast_data(id, "[%s:%s] entered room\n" % addr)

            #Some incoming message from a client
            else:
                # Daten vom Client
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock_id, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

                except Exception as e:
                    #broadcast_data(sock_id, "{} Client {} ist offline".format(sock_id, addr))
                    #print "{} Client {} ist offline".format(sock_id, addr)
                    if sock:
                        sock.close()
                        del CONNECTION_LIST[sock_id]

                    continue

        time.sleep(0.01)
    server_socket.close()
