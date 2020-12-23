import sys
import getopt
from module.util import Validator


def getTotalArgument(args):
    return len(args)


def getHost(args):
    for key, value in args:
        if key in ("-h", "--host"):
            return value
    return None


def getPort(args):
    for key, value in args:
        if key in ("-p", "--port"):
            return value
    return None


def getMode(args):
    for key, value in args:
        if key in ("-c", "--chat"):
            return "CHAT"
        elif key in ("-s", "--scan"):
            return "SCAN"
        elif key in ("-l", "--log"):
            return "LOG"
    return None


def getChatOption(args):
    chat_option = {"HOST": getHost(args), "PORT": getPort(args), "NUMBER": 5, "SERVER": False}
    for key, value in args:
        if key in ("-n", "--number"):
            chat_option["NUMBER"] = value
        elif key in ("-r", "--runServer"):
            chat_option["SERVER"] = True
    return chat_option


def validateChatOption(chat_option):
    if chat_option.get("HOST") is None:
        return "Error: Missing argument '-h | --host'."
    elif chat_option.get("HOST") == "" or \
            not chat_option.get("HOST").count(".") == 3 or \
            not all(Validator.isIPv4(i) for i in chat_option.get("HOST").split(".")):
        return "Error: Invalid argument '-h | --host' format."
    elif chat_option.get("PORT") is None:
        return "Error: Missing argument '-p | --port'."
    elif chat_option.get("PORT") == "" or \
            not Validator.isValidRange(chat_option.get("PORT"), 49152, 65535):
        return "Error: Invalid argument '-p | --port' range."
    elif chat_option.get("NUMBER") == "" or \
            not Validator.isValidRange(chat_option.get("NUMBER"), 1, 10):
        return "Error: Invalid argument '-n | --number' range."
    return None


def getScanOption(args):
    scan_option = {"HOST": getHost(args), "TCP": False, "UDP": False, "FROM": 1, "END": 65535}
    for key, value in args:
        if key in ("-t", "--tcp"):
            scan_option["TCP"] = True
        elif key in ("-u", "--udp"):
            scan_option["UDP"] = True
        elif key in ("-f", "--from"):
            scan_option["FROM"] = value
        elif key in ("-e", "--end"):
            scan_option["END"] = value
    return scan_option


def validateScanOption(scan_option):
    if scan_option.get("HOST") is None:
        return "Error: Missing argument '-h | --host'."
    elif scan_option.get("HOST") == "" or \
            not scan_option.get("HOST").count(".") == 3 or \
            not all(Validator.isIPv4(i) for i in scan_option.get("HOST").split(".")):
        return "Error: Invalid argument '-h | --host' format."
    elif not Validator.isValidRange(scan_option.get("FROM"), 1, 65535):
        return "Error: Invalid argument '-f | --from' range."
    elif not Validator.isValidRange(scan_option.get("END"), 1, 65535) and \
            scan_option.get("END") < scan_option.get("FROM"):
        return "Error: Invalid argument '-e | --end' range."
    return None


def getLogOption(args):
    log_option = {"KEYBOARD": False, "MOUSE": False, "DELAY": 1}
    for key, value in args:
        if key in ("-k", "--keyboard"):
            log_option["KEYBOARD"] = True
        elif key in ("-m", "--mouse"):
            log_option["MOUSE"] = True
        elif key in ("-d", "--delay"):
            log_option["DELAY"] = value
    return log_option


def validateLogOption(log_option):
    if log_option.get("KEYBOARD") is False and log_option.get("MOUSE") is False:
        return "Error: Missing argument '-k | --keyboard' and/or '-m | --mouse'."
    elif not Validator.isValidRange(log_option.get("DELAY"), 1, 10):
        return "Error: Missing argument '-d | --delay'."
    return None


def getAllArgument():
    try:
        args, _ = getopt.getopt(sys.argv[1:],
                                "h:p:cn:rstuf:e:lkmd:",
                                ["host=", "port=", "chat", "number=", "runServer", "scan", "tcp", "udp", "from=",
                                 "end=", "log", "keyboard", "mouse", "delay="])
    except Exception:
        return None

    if getTotalArgument(args) == 0:
        return None

    all_argument = {"ERROR_MESSAGE": None, "MODE": getMode(args), "OPTION": None}

    if all_argument.get("MODE") is None:
        all_argument["ERROR_MESSAGE"] = "Error: Missing argument '-c | --chat' or '-s | --scan' or '-l | --log'."
    else:
        if all_argument.get("MODE") == "CHAT":
            all_argument["OPTION"] = getChatOption(args)
            all_argument["ERROR_MESSAGE"] = validateChatOption(all_argument.get("OPTION"))
        elif all_argument.get("MODE") == "SCAN":
            all_argument["OPTION"] = getScanOption(args)
            all_argument["ERROR_MESSAGE"] = validateScanOption(all_argument.get("OPTION"))
        elif all_argument.get("MODE") == "LOG":
            all_argument["OPTION"] = getLogOption(args)
            all_argument["ERROR_MESSAGE"] = validateLogOption(all_argument.get("OPTION"))

    return all_argument
