from select import select
from tqdm import tqdm
from threading import Thread
from module.helper.PrintHandler import printHeaderCustom
from module.core.chatting.ChattingUtility import *

SOCKET_LIST = []


def broadcastMessage(socket_server, socket_current, message_json, isInfo=False):
    for socket_broadcast in SOCKET_LIST:
        if socket_broadcast != socket_server and socket_broadcast != socket_current:
            try:
                sendEncodeMessage(socket_broadcast, message_json)
            except Exception:
                message_json = {
                    "ADDRESS": getAddress(socket_broadcast),
                    "TYPE": "INFO",
                    "DATA": "[*] Client " + getAddress(socket_broadcast) + " has left the group chat."
                }
                replaceMessage(socket_server, socket_current, message_json.get("DATA"), isInfo=True)
                SOCKET_LIST.remove(socket_broadcast)
                socket_broadcast.close()


def receiveMessageServer(socket_server):
    while True:

        socket_all = None
        try:
            socket_all, _, _ = select(SOCKET_LIST, [], [], 0)
        except Exception:
            for socket_current in SOCKET_LIST:
                socket_current.close()
            socket_server.close()
            exit(1)

        for socket_current in socket_all:

            if socket_current == socket_server:
                socket_client, socket_address = socket_server.accept()
                message_json = {
                    "ADDRESS": getAddress(socket_client),
                    "TYPE": "INFO",
                    "DATA": "[*] Client " + getAddress(socket_client) + " has joined the group chat."
                }
                replaceMessage(socket_server, getAddress(socket_client), message_json.get("DATA"), isInfo=True)
                broadcastMessage(socket_server, socket_client, message_json, isInfo=True)
                SOCKET_LIST.append(socket_client)

            else:
                try:
                    message_client = receiveDecodeMessage(socket_current)
                    if message_client.get("TYPE") == "TEXT":
                        replaceMessage(socket_server, message_client.get("ADDRESS"), message_client.get("DATA"))
                        broadcastMessage(socket_server, socket_current, message_client)

                    elif message_client.get("TYPE") == "SCREENSHOT":
                        pass

                    elif message_client.get("TYPE") == "FILE":
                        message_json = {
                            "ADDRESS": message_client.get("ADDRESS"),
                            "TYPE": "INFO",
                            "DATA": "[*] Client " + message_client.get("ADDRESS") + " sent a file."
                        }
                        replaceMessage(socket_server, message_client.get("ADDRESS"), message_json.get("DATA"), isInfo=True)
                        broadcastMessage(socket_server, message_client.get("ADDRESS"), message_json, isInfo=True)

                        file_name = message_client.get("DATA").split(SEPARATOR)[0]
                        file_path = DIRECTORY_RECEIVE + file_name
                        file_size = int(message_client.get("DATA").split(SEPARATOR)[1])
                        broadcastMessage(socket_server, socket_current, message_client, isInfo=True)

                        progress = tqdm(range(file_size), f" Broadcasting {file_name}", ascii=True)
                        with open(file_path, "wb") as _:
                            for _ in progress:
                                bytes_read = socket_current.recv(MAX_BUFFER_FILE)
                                if not bytes_read:
                                    print("\r")
                                    break
                                for socket_broadcast in SOCKET_LIST:
                                    if socket_broadcast != socket_server and socket_broadcast != socket_current:
                                        socket_broadcast.sendall(bytes_read)
                                progress.update(len(bytes_read))
                        print("\r " + getAddress(socket_server, isLeft=True) + " ", end="")

                except Exception:
                    message_json = {
                        "ADDRESS": getAddress(socket_current),
                        "TYPE": "INFO",
                        "DATA": "[*] Client " + getAddress(socket_current) + " has left the group chat."
                    }
                    replaceMessage(socket_server, socket_current, message_json.get("DATA"), isInfo=True)
                    broadcastMessage(socket_server, socket_current, message_json, isInfo=True)
                    SOCKET_LIST.remove(socket_current)
                    socket_current.close()


def sendMessageServer(socket_server):
    while True:
        message_json = {
            "ADDRESS": getAddress(socket_server, isLeft=True),
            "TYPE": "TEXT",
            "DATA": validateInput(socket_server)
        }

        if len(message_json.get("DATA")) == 0:
            continue

        message_input_split = message_json.get("DATA").split(" ", 1)
        message_command = message_input_split[0]

        if validateCommand(message_command):
            message_command = message_command[1:-1]

            if message_command == "shutdown":
                for socket_current in SOCKET_LIST:
                    socket_current.close()
                socket_server.close()
                exit(1)
            else:
                for socket_current in SOCKET_LIST:
                    if socket_current != socket_server:
                        sendEncodeMessage(socket_current, message_json)
        else:
            for socket_current in SOCKET_LIST:
                if socket_current != socket_server:
                    sendEncodeMessage(socket_current, message_json)


def chattingServer(arguments):
    socket_server = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_PROTOCOL)
    try:
        socket_server.bind((arguments.get("HOST"), int(arguments.get("PORT"))))
    except Exception:
        printHeaderCustom(errorMessage="Unable to create a group chat.")
        return
    socket_server.listen(int(arguments.get("NUMBER")))
    SOCKET_LIST.append(socket_server)

    printHeaderCustom(message="Listening on " + getAddress(socket_server, isLeft=True) + " ")

    receive_thread = Thread(target=receiveMessageServer, args=(socket_server,))
    send_thread = Thread(target=sendMessageServer, args=(socket_server,))
    receive_thread.start()
    send_thread.start()
    receive_thread.join()
    send_thread.join()

    for socket_current in SOCKET_LIST:
        socket_current.close()
    socket_server.close()

