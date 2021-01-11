from sys import exit
from module.helper.FileHandler import autoCreateFiles
from module.helper.PrintHandler import printHelp
from module.helper.ArgumentHandler import getAllArgument
from module.core.chatting.Chatting import chatting
from module.core.scanning.Scanning import scanning
from module.core.logging.Logging import logging

if __name__ == '__main__':

    autoCreateFiles()

    arguments = getAllArgument()

    if arguments is None:
        printHelp()
        exit(0)
    elif arguments.get("ERROR_MESSAGE") is not None:
        printHelp(arguments["ERROR_MESSAGE"])
        exit(0)

    if arguments.get("MODE") == "CHAT":
        chatting(arguments.get("OPTION"))
    elif arguments.get("MODE") == "SCAN":
        scanning(arguments.get("OPTION"))
    elif arguments.get("MODE") == "LOG":
        logging(arguments.get("OPTION"))
