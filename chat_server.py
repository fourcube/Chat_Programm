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
import protocol
import time
import signal
from threading import Thread

from crypto import encryptedMessage, decryptedMessage

def current_millis():
    return int(round(time.time() * 1000))

last_ping_timestamp = 0
PING_INTERVAL = 1
PING=True

# Client alle PING_INTERVAL Sekunden anpingen
def ping_clients(broadcastFn, server_socket_id):
    global PING
    while PING:
        broadcastFn(server_sock_id, protocol.pack_ping())
        time.sleep(PING_INTERVAL)

# Ping Schleife beenden
def stop_ping(_,d):
    global PING
    PING=False

# Remove client from CONNECTION_LIST if exists
def remove_client (id):
    if id in CONNECTION_LIST:
	del CONNECTION_LIST[id]

# Function to broadcast chat messages to all connected clients
def broadcast_data (sock_id, message, recurse=True):
    print "broadcasting %s" % message
    #Do not send the message to master socket and the client who has sent us the message
    for id, socket in CONNECTION_LIST.items():
        if id != server_socket.fileno() and id != sock_id:
            try:
                socket.send(message)
            except Exception as e:
                if recurse:
                    offlineMsg = protocol.pack_text("Client %s is offline." % id)
                    broadcast_data(
                        sock_id = id,
                        message = encryptedMessage(offlineMsg, 6),
                        recurse = False) # If "broadcast_data" throws an
                                         # Exception again, do not recurse
                                         # any deeper
                remove_client(id)

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

    t = Thread(target=ping_clients, args=(broadcast_data,server_sock_id))
    t.start()

    # CTRL+C Stoppt the Ping Thread
    signal.signal(signal.SIGINT, stop_ping)


    print "Server wurde gestartet, Port: " + str(PORT)
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST.keys(),[],[])

        for sock_id in read_sockets:
            sock = CONNECTION_LIST.get(sock_id, None)
            if sock is None:
                continue

            # New connection
            if sock_id == server_sock_id:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                id = sockfd.fileno()

                CONNECTION_LIST[id] = sockfd
                print "{} Client {} connected".format(id, addr)

                msg = protocol.pack_text("[%s:%s] entered room." % addr)
                broadcast_data(id, encryptedMessage(msg, 6))

            # Some incoming message from a client
            else:
                # Data received from client
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        print data
                        # simply broadcast
                        broadcast_data(sock_id, data)


                except Exception as e:
                    print "{} Client {} ist offline".format(sock_id, addr)
                    if sock:
                        sock.close()
                    remove_client(id)

                    continue

        time.sleep(0.01)
    server_socket.close()
