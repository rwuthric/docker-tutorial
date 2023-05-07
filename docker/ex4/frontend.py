import socket
import sys

"""
Front-end server

Listens to port 10000 for incoming connections
When getting data, will query the backend in order to convert the prize of the item to USD
"""

def queryBackend(data):
    """
    Queries the backend server to convert CAD to USD
    """
    backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend.connect(('backend', 3000))
    backend.sendall(data)
    answ = backend.recv(16)
    backend.close()
    return answ
    

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind all interfaces to the port
server_address = ('0.0.0.0', 10000)
print('Starting front-end server on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection ...')
    connection, client_address = sock.accept()
    
    try:
        print('Connection from', client_address)
        connection.sendall(b'Which product you wish to buy ?\n')
        connection.sendall(b'1. A laptop\n')
        connection.sendall(b'2. A PC\n')
        connection.sendall(b'3. A server\n')

        # Receive the data
        while True:
            data = connection.recv(16).decode("utf-8").strip()
            if data:
                print('  Received "%s"' % data)
                answ = ''
                match data:
                    case '1':
                      answ = queryBackend(b'1100');
                    case '2':
                      answ = queryBackend(b'2400');
                    case '3':
                      answ = queryBackend(b'35000');
                    case _:
                      connection.sendall(b'Wrong selection. Please try again');
                
                if answ!='':
                    answ = 'Today your item costs ' + answ.decode("utf-8").strip() + ' USD\n'
                    connection.sendall(answ.encode())
                
            else:
                print('  no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
       
