import socketio

sio = socketio.Client()

connected_devices = []

@sio.event
def connect():
    print('connection established')

    while True:
        message = input("Message:\n")
        device = int(input("Device:\n"))
        msg_data = {
            "message":message,
            "target_sid":connected_devices[device],
            "type":"generic_message"
        }
        sio.emit("rcv_message", msg_data)

@sio.event
def rcv_message(data):
    if (data['type'] == 'interface_add_device'):
        print('added device', data['sid'])
        connected_devices.append(data['sid'])
    elif (data['type'] == 'interface_remove_device'):
        print('removed device', data['sid'])
        connected_devices.remove(data['sid'])

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
