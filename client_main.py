import socketio
import curses

sio = socketio.Client()

connected_devices = []

latest_message = ""

win: curses.window

def message_input():
    global win
    text = ""
    while True:
        draw_header()
        y = len(connected_devices)+2
        win.move(y,0)
        win.deleteln()
        win.move(y+1,0)
        win.deleteln()
        win.addstr(y, 0, "Message to send:")
        win.addstr(y+1, 0, text)
        win.refresh()
        key = win.getkey()
        if (key in ('KEY_BACKSPACE', '\b', '\x7f')):
            text = text[:-1]
        elif (key.isalpha() or key.isnumeric() or key == ' ' or key == '_'):
            text += key
        elif (key == '\n'):
            break
    return text

def deviceid_input():
    global win
    text = ""
    while True:
        draw_header()
        y = len(connected_devices)+2
        win.move(y,0)
        win.deleteln()
        win.move(y+1,0)
        win.deleteln()
        win.addstr(y, 0, "Device to send to:")
        win.addstr(y+1, 0, text)
        win.refresh()
        key = win.getkey()
        if (key in ('KEY_BACKSPACE', '\b', '\x7f')):
            text = text[:-1]
        elif (key.isnumeric()):
            text += key
        elif (key == '\n'):
            break
    return int(text)

def draw_header():
    win.erase()

    win.addstr(0,0,"Connected devices:")
    for i in range(len(connected_devices)):
        win.addstr(i+1,0,"["+str(i)+"] " + connected_devices[i])

@sio.event
def connect():
    global win
    print('connection established')

    win = curses.initscr()
    win.keypad(True)
    curses.noecho()
    curses.cbreak()

    while True:
        draw_header()
        message = message_input()
        draw_header()
        device = deviceid_input()
        msg_data = {}
        if (message == 'toggle_light'):
            msg_data = {
                "sid":connected_devices[device],
                "type":"toggle_light"
            }
        else:
            msg_data = {
                "message":message,
                "sid":connected_devices[device],
                "type":"generic_message"
            }
        sio.emit("rcv_message", msg_data)

@sio.event
def rcv_message(data):
    global win
    if (data['type'] == 'interface_add_device'):
        connected_devices.append(data['sid'])
    elif (data['type'] == 'interface_remove_device'):
        connected_devices.remove(data['sid'])

@sio.event
def disconnect():
    curses.endwin()
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
