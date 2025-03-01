import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

    while (True):
        message = input("message here pls ty\n")
        sio.emit("my_message", {"msg_data":message,"sid":sio.sid})

@sio.event
def my_message(data):
    if (data['sid'] != sio.sid):
        print('message from ' + data['sid'] + ' with ', data)
    #sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()
