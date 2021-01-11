from os import path, makedirs

def autoCreateFiles():

    if not path.exists("files"):
        makedirs("files")

    if not path.exists("files/log"):
        makedirs("files/log")
    if not path.exists("files/receive"):
        makedirs("files/receive")
    if not path.exists("files/send"):
        makedirs("files/send")