import socket
import sys
import requests

"""
Back-end server

Listens to port 3000 for incoming connections
When getting data, converts it to USD and sends it back
"""


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind all interfaces to the port
server_address = ('0.0.0.0', 3000)
print('Starting back-end server on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('Waiting for a connection ...')
    connection, client_address = sock.accept()
    
    try:
        print('Connection from', client_address)
        
        # Currency converter API
        url = "https://open.er-api.com/v6/latest/USD"
        req = requests.get(url)
        exchange_rate = req.json()['rates']['CAD']

        # Receive the data
        while True:
            prize = connection.recv(16).decode("utf-8").strip()
            if prize:
                print('  Received "%s"' % prize)
                USD_prize = '{:.2f}\n'.format(float(prize)*exchange_rate)
                connection.sendall(USD_prize.encode())
            else:
                print('  no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()
       
