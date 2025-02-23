import sys
from datetime import datetime
from colored import fg, attr
# try:
#     from colored import fg, attr
# except ModuleNotFoundError:
#     import subprocess
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colored'])
#     from colored import fg, attr


def printHeader():
    print("%s" % (fg('dark_goldenrod')), end="")
    print("  _____     __   __                                     _   _ ")
    print(" |  __ \\    \\ \\ / /                                    | | (_) ")
    print(" | |__) |___ \\ V / _ __  _   _ _ __ ___   ___ _ __ __ _| |_ _  ___  _ __ ")
    print(" |  _  // _ \\ > < | '_ \\| | | | '_ ` _ \\ / _ \\ '__/ _` | __| |/ _ \\| '_ \\ ")
    print(" | | \\ \\  __// . \\| | | | |_| | | | | | |  __/ | | (_| | |_| | (_) | | | | ")
    print(" |_|  \\_\\___/_/ \\_\\_| |_|\\__,_|_| |_| |_|\\___|_|  \\__,_|\\__|_|\\___/|_| |_| ")
    print("%s Version 1.0%s\n" % (fg('light_salmon_3a'), attr('reset')))


def printError(errorMessage):
    print("%s [!] %s %s" % (fg('red'), errorMessage, attr('reset')))


def printInformation(message):
    print("%s [!] %s %s" % (fg('orange_1'), message, attr('reset')))


def printHeaderCustom(message=None, errorMessage=None):
    printHeader()

    if errorMessage is not None:
        printError(errorMessage)
    else:
        current_date_time = datetime.today().strftime('%d-%b-%Y %H:%M:%S')
        print("%s [*] %s %s" % (fg('blue_3a'), message + "at " + current_date_time, attr('reset')), end="\n\n")


def printHelp(errorMessage=None):
    printHeader()

    if errorMessage is not None:
        printError(errorMessage + "\n")

    file_name = sys.argv[0]

    print("%s" % (fg('blue_3a')), end="")
    print(" Usage: %s (-c -h <ip_address> -p <port> [-r [-n <total_connection>]] | "
          "-s -h <ip_address> [-f <port>] [-e <port>] | -l (-k | -m)\n" % file_name)

    print("%s" % (fg('dodger_blue_2')), end="")
    print(" Options:")
    print("   -h <ip_address>, --host=<ip_address>\t\t\t IP address (e.g. 127.0.0.1)")
    print("   -p <port_number>, --port=<port_number>\t\t Port number to use/connect (e.g. 60000)")
    print("   -c, --chat\t\t\t\t\t\t Set application mode to group chat")
    print("   -n <total_connection>, --number=<total_connection>\t Maximum number of connection (default: 5)")
    print("   -r, --runServer\t\t\t\t\t Run as server")
    print("   -s, --scan\t\t\t\t\t\t Set application mode to port scanning")
    print("   -f <port>, --from=<port>\t\t\t\t Set first port constraint (default: 0)")
    print("   -e <port>, --end=<port>\t\t\t\t Set last port constraint (default: 65535)")
    print("   -l, --log\t\t\t\t\t\t Set application mode to logging")
    print("   -k, --keyboard\t\t\t\t\t Enable keyboard logging")
    print("   -m, --mouse\t\t\t\t\t\t Enable mouse logging\n")

    print("%s" % (fg('deep_sky_blue_4b')), end="")
    print(" Example:")
    print("   Script for create a server chatting application on 127.0.0.1 port 60000 with maximum 8 number of "
          "client connections")
    print("      {} -c -h 127.0.0.1 -p 60000 -r -n 8".format(file_name))
    print("      {} --chat --host=127.0.0.1 --port=60000 --runServer --number=8".format(file_name))
    print("   Script for client to connect to server chatting application on 127.0.0.1 port 60000")
    print("      {} -c -h 127.0.0.1 -p 60000".format(file_name))
    print("      {} --chat --host=127.0.0.1 --port=60000".format(file_name))
    print("   Script for port scanning on 127.0.0.1 from port 100 until 1000")
    print("      {} -s -h 127.0.0.1 -f 100 -e 1000".format(file_name))
    print("      {} --scan --host=127.0.0.1 --from=100 --end=1000".format(file_name))
    print("   Script for key logger and mouse logger")
    print("      {} -l -k -m".format(file_name))
    print("      {} --log --keyboard --mouse".format(file_name))
    print("%s" % (attr('reset')), end="")

