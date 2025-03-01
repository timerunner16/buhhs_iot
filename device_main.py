import socketio

sio = socketio.Client()

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
    if (data['sid'] == sio.get_sid()):
        print("hi im the target device")
    print(data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()