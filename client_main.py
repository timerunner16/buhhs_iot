import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

    while (True):
        message = input("Message:\n")
        if (message == 'toggle'):
            sio.emit(
                "message", {
                    "msg_data":message,
                    "sid":sio.sid,
                    "type":"toggle"
                }
            )
        else:
            sio.emit(
                "message", {
                    "msg_data":message,
                    "sid":sio.sid,
                    "type":"message"
                }
            )

@sio.event
def message(data):
    if (data['sid'] != sio.sid):
        print('message from ' + data['sid'])
        print('message: ' + data['message'])
        print('type: ' + data['type'])

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
