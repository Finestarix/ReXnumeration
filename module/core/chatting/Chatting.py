from module.core.chatting.ChattingClient import chattingClient
from module.core.chatting.ChattingServer import chattingServer

def chatting(arguments):
    if arguments.get("SERVER"):
        chattingServer(arguments)
    else:
        chattingClient(arguments)
