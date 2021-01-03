import sys
import socket
import select
from threading import Thread
from module.helper.PrintHandler import printHeaderChatting, printError, printInformation

MAX_BUFFER = 1024

SOCKET_ADDRESS_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM

SOCKET_LIST = []

sock_list = []
stored = []


def getAddress(socket_current, isLeft=False):
    host_client, port_client = socket_current.getsockname() if isLeft else socket_current.getpeername()
    return " " + str(host_client) + ":" + str(port_client) + " "


def broadcastMessage(socket_server, socket_current, message, isInfo=False):
    for socket_broadcast in SOCKET_LIST:
        if socket_broadcast != socket_server and socket_broadcast != socket_current:
            message = "|" + message if isInfo else getAddress(socket_current) + "| " + message
            message_encode = message.encode()

            try:
                socket_broadcast.send(message_encode)
            except Exception:
                server_message = "[*] Client" + getAddress(socket_current) + \
                                 "has left the group chat."
                print("\r " + server_message + "\n" +
                      getAddress(socket_server, isLeft=True), end="")
                broadcastMessage(socket_server, socket_current, server_message, isInfo=True)
                SOCKET_LIST.remove(socket_broadcast)
                socket_broadcast.close()


def receiveMessageServer(socket_server):
    while True:

        socket_all, _, _ = select.select(SOCKET_LIST, [], [], 0)

        for socket_current in socket_all:

            if socket_current == socket_server:
                socket_client, socket_address = socket_server.accept()
                SOCKET_LIST.append(socket_client)
                server_message = "[*] Client" + getAddress(socket_client) + \
                                 "has joined the group chat."
                print("\r " + server_message + "\n" +
                      getAddress(socket_server, isLeft=True), end="")
                broadcastMessage(socket_server, socket_client, server_message, isInfo=True)

            else:
                try:
                    message_client = socket_current.recv(MAX_BUFFER)
                    if message_client:
                        message_client = message_client.decode()
                        print("\r" + getAddress(socket_current) + message_client + "\n" +
                              getAddress(socket_server, isLeft=True), end="")
                        broadcastMessage(socket_server, socket_current, message_client)

                except Exception:
                    server_message = "[*] Client" + getAddress(socket_current) + \
                                     "has left the group chat."
                    print("\r " + server_message + "\n" +
                          getAddress(socket_server, isLeft=True), end="")
                    broadcastMessage(socket_server, socket_current, server_message, isInfo=True)
                    SOCKET_LIST.remove(socket_current)
                    socket_current.close()


def sendMessageServer(socket_server):
    while True:
        message_input = ""
        try:
            while len(message_input) <= 0 or len(message_input) >= 1000:
                print(getAddress(socket_server, isLeft=True), end="")
                message_input = input()
                if len(message_input) <= 0 or len(message_input) >= 1000:
                    printError("Invalid input.")
        except Exception:
            print("")
            continue

        for socket_current in SOCKET_LIST:
            if socket_current != socket_server:
                message = getAddress(socket_server, isLeft=True).strip() + "|" + message_input
                message_encode = message.encode()

                try:
                    socket_current.send(message_encode)
                except Exception:
                    printError("Connection closed A.")
                    SOCKET_LIST.remove(socket_current)
                    socket_current.close()


def receiveMessageClient(socket_client):
    while True:
        try:
            message = socket_client.recv(MAX_BUFFER)
        except Exception:
            print("\r", end="")
            printError("Group chat disbanded.")
            socket_client.close()
            sys.exit(1)

        message_decode = message.decode().split("|", 1)
        address = message_decode[0]
        message_only = message_decode[1]
        print("\r " + address + message_only + "\n" + getAddress(socket_client, isLeft=True), end="")


def sendMessageClient(socket_client):
    while True:
        message = ""
        try:
            while len(message) <= 0 or len(message) >= 1000:
                print(getAddress(socket_client, isLeft=True), end="")
                message = input()
                if len(message) <= 0 or len(message) >= 1000:
                    printError("Invalid input.")
        except Exception:
            print("")
            continue
        message_encode = message.encode()

        try:
            socket_client.send(message_encode)
        except Exception:
            print("\r", end="")
            printError("Group chat disbanded.")
            socket_client.close()
            sys.exit(1)


def chattingServer(arguments):
    host_server = arguments.get("HOST")
    port_server = int(arguments.get("PORT"))
    total_queue = int(arguments.get("NUMBER"))

    socket_server = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_PROTOCOL)
    try:
        socket_server.bind((host_server, port_server))
    except Exception:
        printHeaderChatting(errorMessage="Unable to create a group chat.")
        return
    socket_server.listen(total_queue)

    printHeaderChatting(message="Listening on" + getAddress(socket_server, isLeft=True))
    SOCKET_LIST.append(socket_server)

    receive_thread = Thread(target=receiveMessageServer, args=(socket_server,))
    receive_thread.start()
    send_thread = Thread(target=sendMessageServer, args=(socket_server,))
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    socket_server.close()
    for socket_current in SOCKET_LIST:
        socket_current.close()


def chattingClient(arguments):
    host_client = arguments.get("HOST")
    port_client = int(arguments.get("PORT"))

    socket_client = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_PROTOCOL)
    try:
        socket_client.connect((host_client, port_client))
    except Exception:
        printHeaderChatting(errorMessage="Unable to join the group chat.")
        return

    printHeaderChatting(message="Connected to" + getAddress(socket_client))

    receive_message = Thread(target=receiveMessageClient, args=(socket_client,))
    receive_message.start()
    send_message = Thread(target=sendMessageClient, args=(socket_client,))
    send_message.start()

    receive_message.join()
    send_message.join()

    socket_client.close()


def chatting(arguments):
    if arguments.get("SERVER"):
        chattingServer(arguments)
    else:
        chattingClient(arguments)


# TODO: Open Windows File Explorer https://stackoverflow.com/questions/281888/open-explorer-on-a-file
# TODO: Create Send File using ProgressBar https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# TODO: Screenshot
# TODO: Learn PyHook
