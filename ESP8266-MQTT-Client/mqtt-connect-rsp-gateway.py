import usocket
import sys
import machine

led = machine.Pin(2, machine.Pin.OUT)

ADDR = '192.168.12.40'
PORT = 10000
# Create a UDP socket
client_sock = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = 'led-light'
if not device_id:
    sys.exit('The device id must be specified.')

print('Bringing up device {}'.format(device_id))


def SendCommand(sock, message):
    print('sending "{}"'.format(message))
    sock.sendto(message.encode(), server_address)

    # Receive response
    print('waiting for response')
    response = sock.recv(4096)
    print('received: "{}"'.format(response))

    return response


def MakeMessage(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(
            device_id, action, data)
    else:
        return '{{ "device" : "{}", "action":"{}" }}'.format(
            device_id, action)


def RunAction(action, data=''):
    global client_sock
    message = MakeMessage(device_id, action, data)
    if not message:
        return
    print('Send data: {} '.format(message))
    event_response = SendCommand(client_sock, message)
    print('Response: {}'.format(event_response))


try:
    RunAction('detach')
    RunAction('attach')
    RunAction('event', 'LED is online')
    RunAction('subscribe')

    while True:
        response = client_sock.recv(4096).decode('utf8')
        print('Client received {}'.format(response))
        if response.upper() == 'ON' or response.upper() == b'ON':
            led.off()
            sys.stdout.write('\r>> ' +
                             " LED is ON " + ' <<')
            sys.stdout.flush()
        elif response.upper() == "OFF" or response.upper() == b'OFF':
            led.off()
            sys.stdout.write('\r >>' + 
                             ' LED is OFF ' + ' <<')
            sys.stdout.flush()
        else:
            print('Invalid message {}'.format(response))

finally:
    print('closing socket', file=sys.stderr)
    client_sock.close()
