import socketio

sio = socketio.Client()

enabled: bool = False

@sio.event
def connect():
    print('connection established')

    msg_data = {
        'type':'register_device',
        'message':'emulated_device'
    }
    print(msg_data)
    sio.emit("rcv_message", msg_data)
    print("done")

@sio.event
def rcv_message(data):
    global enabled
    if (data['sid'] == sio.get_sid()):
        print("Current device is targeted by command")
        if (data['type'] == 'toggle_light'):
            enabled = not enabled
            print("Light is now " + ("enabled" if enabled else "disabled"))
        else:
            print(data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()