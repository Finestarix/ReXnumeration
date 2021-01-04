import socket
from sys import exit
from progress.bar import Bar
from csv import DictReader
from threading import Thread
from module.helper.PrintHandler import printHeaderChatting, printError, printInformation

SOCKET_ADDRESS_FAMILY = socket.AF_INET
SOCKET_PROTOCOL_TCP = socket.SOCK_STREAM
SOCKET_PROTOCOL_UDP = socket.SOCK_DGRAM

TCP_FILE = "./dataset/tcp.csv"
TCP_CSV = DictReader(open(TCP_FILE))
TCP_LIST = []


def scanningPortTCP(host, port, SOCKET_PROTOCOL, progress):
    socket_current = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_PROTOCOL)
    socket.setdefaulttimeout(2)

    result = socket_current.connect_ex((host, port))
    if result == 0:
        description = "Unknown Service"
        for tcp_data in DictReader(open(TCP_FILE)):
            if int(tcp_data["port"]) == port:
                description = tcp_data["description"]
        TCP_LIST.append({"port": port, "description": description})
    socket_current.close()

    progress.next()

def scanningTCP(arguments):
    try:
        thread_list = []
        progress = Bar(f"\r Scanning {arguments.get('HOST')}",
                       max=int(arguments.get("END")) - int(arguments.get("FROM")))
        for port in range(int(arguments.get("FROM")), int(arguments.get("END"))):
            scanning_thread = Thread(target=scanningPortTCP,
                                     args=(arguments.get("HOST"), port, SOCKET_PROTOCOL_TCP, progress,))
            scanning_thread.start()
            thread_list.append(scanning_thread)
        for thread in thread_list:
            thread.join()
        progress.finish()

        print("")
        print(" +%s+%s+" % ("-" * 10, "-" * 47))
        print(" | {:<8} | {:<45} |".format("Port", "Description"))
        print(" +%s+%s+" % ("-" * 10, "-" * 47))
        for port in TCP_LIST:
            print(" | {:<8} | {:<45} |".format(port["port"], port["description"]))
        print(" +%s+%s+" % ("-" * 10, "-" * 47))

    except Exception:
        printError("Scanning terminated.")
        exit(1)


def scanning(arguments):
    printHeaderChatting(message="Scanning " + arguments.get("HOST") + " ")
    scanningTCP(arguments)
