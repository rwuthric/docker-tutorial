import socket
import sys

"""
Python echo server

Listen to port 10000 for incoming connections
When getting data, will send it back to the sender
"""

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind all interfaces to the port
server_address = ('0.0.0.0', 10000)
print('Starting echo server on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection ...')
    connection, client_address = sock.accept()
    
    try:
        print('Connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data:
                print('  Received "%s"' % data)
                connection.sendall(data)
            else:
                print('  no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
       
