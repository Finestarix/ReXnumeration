import socket
from sys import exit
from json import loads, dumps
from module.helper.PrintHandler import printError

SOCKET_ADDRESS_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM

MIN_TEXT = 0
MAX_TEXT = 500
MAX_BUFFER = 1024
MAX_BUFFER_FILE = 1

DIRECTORY_SEND = "./files/send/"
DIRECTORY_RECEIVE = "./files/receive/"
DIRECTORY_PICTURE = "./files/receive/screenshot/"
SEPARATOR = "<SEPARATOR>"


def replaceMessage(socket_current, address, message, isInfo=False):
    if isInfo:
        print("\r " + message + "\n " +
              getAddress(socket_current, isLeft=True) + " ", end="")
    else:
        print("\r " + address + " " + message + "\n " +
              getAddress(socket_current, isLeft=True) + " ", end="")


def validateInput(socket_client):
    message = ""
    try:
        while len(message) <= MIN_TEXT or len(message) >= MAX_TEXT:
            print(" " + getAddress(socket_client, isLeft=True) + " ", end="")
            message = ""
            message = input()
            if len(message) <= MIN_TEXT or len(message) >= MAX_TEXT:
                printError("Invalid input.")
    except Exception:
        printError("Invalid input.")
    return message


def validateCommand(message_command):
    return len(message_command) > 2 and message_command[0] == "[" and message_command[-1] == "]"


def getAddress(socket_current, isLeft=False):
    host_client, port_client = socket_current.getsockname() if isLeft else socket_current.getpeername()
    return str(host_client) + ":" + str(port_client)


def sendEncodeMessage(socket_current, message_json):
    message_encode = dumps(message_json).encode()
    try:
        socket_current.send(message_encode)
    except Exception:
        print("\r", end="")
        printError("You has left the group chat.")
        socket_current.close()
        exit(1)


def receiveDecodeMessage(socket_current):
    message = socket_current.recv(MAX_BUFFER)
    return loads(message.decode())
