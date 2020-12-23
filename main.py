from module.helper import PrintHandler
from module.helper.ArgumentHandler import getAllArgument

if __name__ == '__main__':
    all_arguments = getAllArgument()

    if all_arguments is None:
        PrintHandler.printHelp()
        exit(0)
    elif all_arguments.get("ERROR_MESSAGE") is not None:
        PrintHandler.printHelp(all_arguments["ERROR_MESSAGE"])
        exit(0)





