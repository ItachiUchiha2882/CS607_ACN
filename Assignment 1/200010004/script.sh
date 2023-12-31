#!/bin/bash

# Instructions to run:
# 1. First start the server code before the client code in two different terminals.
# 2. Run "bash script.sh server" and "bash script.sh client" in separate terminals.
# 3. # To run it mannally, use the following commands:
  # Server Usage: python3 u2.py -p <port-no>
  # Client Usage: python3 u1.py -s <server_ip> -p <server_port>

# Default values for port number and IP address
port=1234
ip_addr="10.196.77.134"  # Change this to the IP address of the server

# Check the argument provided to determine whether to run the server or client
if [ $1 == "server" ]; then
    # Start the server
    python3 u2.py -p $port;
elif [ $1 == "client" ]; then
    # Start the client with the specified server IP and port
    python3 u1.py -s $ip_addr -p $port;
fi