import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

connected_devices = []

@sio.event
def connect(sid, environ):
    print('connect', sid)

@sio.event
def rcv_message(sid, data):
    print("message", sid, data)
    msg_data = {}
    if (data['type'] == 'register_device'):
        msg_data = {
            'type':'interface_add_device',
            'sid':sid
        }
    elif (data['type'] == 'remove_device'):
        msg_data = {
            'type':'interface_remove_device',
            'sid':sid
        }
    elif (data['type'] == 'generic_message'):
        msg_data = {
            'type':'generic_message',
            'sid':data['sid'],
            'message':data['message']
        }
    else:
        msg_data = data
    sio.emit('rcv_message', msg_data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    msg_data = {'type':'remove_device'}
    rcv_message(sid, msg_data)
    
if (__name__ == '__main__'):
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)