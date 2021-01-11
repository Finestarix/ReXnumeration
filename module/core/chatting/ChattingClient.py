from os import path, makedirs
from tqdm import tqdm
from time import sleep
from os import path
from uuid import uuid4
from autopy import bitmap
from threading import Thread
from module.core.chatting.ChattingUtility import *
from module.helper.PrintHandler import printHeaderCustom, printError, printInformation


def sendScreenshotClient(socket_client, message_json):
    file_name = str(uuid4()) + ".png"
    file_path = DIRECTORY_SEND + file_name

    ss = bitmap.capture_screen()
    if not path.exists(DIRECTORY_SEND):
        makedirs(DIRECTORY_SEND)
    ss.save(file_path)

    sendFileClient(socket_client, file_name, message_json)


def sendFileClient(socket_client, file_name, message_json):
    file_path = DIRECTORY_SEND + file_name

    if not path.isfile(file_path):
        printError("File not found !")
        return

    file_size = path.getsize(file_path)

    message_json["TYPE"] = "FILE"
    message_json["DATA"] = file_name + SEPARATOR + str(file_size)
    sendEncodeMessage(socket_client, message_json)

    sleep(1)
    progress = tqdm(range(file_size), f" Sending {file_name}", ascii=True)
    with open(file_path, "rb") as f:
        for _ in progress:
            bytes_read = f.read(MAX_BUFFER_FILE)
            if not bytes_read:
                print("\r")
                break
            socket_client.sendall(bytes_read)
            progress.update(len(bytes_read))


def receiveMessageClient(socket_client):
    while True:
        message = None
        try:
            message = receiveDecodeMessage(socket_client)
        except Exception:
            print(end="\n\n")
            printError("Connection disconnected.")
            socket_client.close()
            exit(1)
        if message.get("TYPE") == "INFO" or message.get("TYPE") == "TEXT":
            replaceMessage(socket_client, message.get("ADDRESS"), message.get("DATA"),
                           isInfo=True if message.get("TYPE") == "INFO" else False)
        elif message.get("TYPE") == "FILE":
            file_name = message.get("DATA").split(SEPARATOR)[0]
            file_path = DIRECTORY_RECEIVE + file_name
            file_size = int(message.get("DATA").split(SEPARATOR)[1])

            progress = tqdm(range(file_size), f" Receiving {file_name}", ascii=True)
            with open(file_path, "wb") as f:
                for _ in progress:
                    bytes_read = socket_client.recv(MAX_BUFFER_FILE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))
            print("\r " + getAddress(socket_client, isLeft=True) + " ", end="")


def sendMessageClient(socket_client):
    while True:
        message_json = {
            "ADDRESS": getAddress(socket_client, isLeft=True),
            "TYPE": "TEXT",
            "DATA": validateInput(socket_client)
        }

        if len(message_json.get("DATA")) == 0:
            continue

        message_input_split = message_json.get("DATA").split(" ", 1)
        message_command = message_input_split[0]

        if validateCommand(message_command):
            message_command = message_command[1:-1]

            if message_command == "shutdown":
                socket_client.close()
                exit(1)
            elif message_command == "screenshot":
                sendScreenshotClient(socket_client, message_json)
                pass
            elif message_command == "file":
                if len(message_input_split) == 1:
                    printError("Invalid file.")
                    continue

                sendFileClient(socket_client, message_input_split[1], message_json)
            else:
                sendEncodeMessage(socket_client, message_json)
        else:
            sendEncodeMessage(socket_client, message_json)


def chattingClient(arguments):
    socket_client = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_PROTOCOL)
    try:
        socket_client.connect((arguments.get("HOST"), int(arguments.get("PORT"))))
    except Exception:
        printHeaderCustom(errorMessage="Unable to join the group chat.")
        return

    printHeaderCustom(message="Connected to " + getAddress(socket_client) + " ")

    receive_message = Thread(target=receiveMessageClient, args=(socket_client,))
    send_message = Thread(target=sendMessageClient, args=(socket_client,))
    receive_message.start()
    send_message.start()
    receive_message.join()
    send_message.join()

    socket_client.close()
