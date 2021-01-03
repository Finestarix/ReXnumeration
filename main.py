from module.helper.PrintHandler import printHelp
from module.helper.ArgumentHandler import getAllArgument
from module.core.Chatting import chatting

if __name__ == '__main__':
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
        pass
    elif arguments.get("MODE") == "LOG":
        pass






