import socket
import sys
import threading
import os
import queue

# Function to receive messages
def receive_messages(client_socket, message_queue):
    while True:
        # store the message and the address of the sender
        data, addr = client_socket.recvfrom(1024)
        message = data.decode()
        message_queue.put(("U2", message))
        print("\rU2:", message)
        print("U1:", end=" ", flush=True)  # Print U1: without a newline

        if message.lower() in ["exit", "quit"]:
            print("Ending conversation...")
            os._exit(2)

# Function to collect the address of the sender at the start of the conversation
def address_collection(client_socket, server_ip, server_port, message_queue):
    message = "7jFp$KlQz2E5xP&v1YnR9Gy@U0W#oAqBcZrD8sIt6Xw3VhLmN4eSfTgOuHbMaCi"
    client_socket.sendto(message.encode(), (server_ip, server_port))
    message_queue.put(("U1", message))

# Fuction to send messages
def send_messages(client_socket, server_ip, server_port, message_queue):
    while True:
        # get the reply and send it to the address of the sender
        message = input("U1: ")
        client_socket.sendto(message.encode(), (server_ip, server_port))
        message_queue.put(("U1", message))
        # print("\rU1:", message)  # Overwrite the previous U1: message
        # print("U1:", end=" ", flush=True)  # Print U1: without a newline

        if message.lower() in ["exit", "quit"]:
            print("Ending conversation...")
            os._exit(1)

# Main function
def main():
    # Check if the command line arguments are valid
    if len(sys.argv) != 5 or sys.argv[1] != "-s" or sys.argv[3] != "-p":
        print("Usage: python3 u1.py -s <server_ip> -p <server_port>")
        sys.exit(0)

    # Get the server ip and port number from command line arguments
    server_ip = sys.argv[2]
    server_port = int(sys.argv[4])

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("U1 is connected to", server_ip, "on port", server_port)
    print("Type 'exit' or 'quit' to end the conversation.")

    # create a queue to store the messages
    message_queue = queue.Queue()
    # collect the address of the sender
    address_collection(client_socket, server_ip, server_port, message_queue)

    # create two threads to send and receive messages
    sending_thread = threading.Thread(target=send_messages, args=(client_socket, server_ip, server_port, message_queue))
    receiving_thread = threading.Thread(target=receive_messages, args=(client_socket, message_queue))

    sending_thread.start()
    receiving_thread.start()

if __name__ == "__main__":
    main()