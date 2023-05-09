import socket
import sys
import datetime

"""
Python TCP/IP server

Listen to port 10000 for incoming connections
When getting a connection will log the IP in a log file
"""

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind all interfaces to the port
server_address = ('0.0.0.0', 10000)
print('Starting TCP/IP server on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection ...')
    connection, client_address = sock.accept()
    
    try:
        print('Connection from', client_address)
        now = datetime.datetime.now()
        # log connection
        with open("logs/log.txt", "a") as logfile:
            logfile.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] " + str(client_address) + "\n")
        
        # Welcome message
        connection.sendall(b'Welcome\nTo quit type "bye".\n')

        # Receive data
        while True:
            data = connection.recv(16).decode("utf-8").strip()
            if data:
                print('  Received "%s"' % data)
                if data=='bye':
                    connection.sendall(b'Thank you.\nHope to see you again soon\n')
                    break
            else:
                print('  no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
       
