__package__ = "modelconductor"
# !/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

_EVENT = None
_QUEUE = None

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    # name = client.recv(BUFSIZ).decode("utf8")
    # clients[client] = name

    while True:
        headers = b''
        msg = b''
        # make sure header is received completely
        while len(headers) < HEADERSIZE:
            headers += client.recv(HEADERSIZE)

        # handle overshoot
        msg += headers[HEADERSIZE:]
        headers = headers[:HEADERSIZE]

        # determine length of stuff to be received
        msglen = int(headers)

        while True:
            receive_at_most = msglen - len(msg)
            if receive_at_most == 0:
                break
            msg += client.recv(receive_at_most)

        print("Received message: ", msg[0:50])
        _QUEUE.put(msg)


clients = {}
addresses = {}

HOST = ''
PORT = 33003
BUFSIZ = 64
ADDR = (HOST, PORT)
HEADERSIZE = 10

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def run(event, queue):
    global _EVENT
    global _QUEUE
    _EVENT = event
    _QUEUE = queue
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()