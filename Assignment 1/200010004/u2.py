import socket
import sys
import threading
import os
import queue

addr = ""

# Function to receive messages
def receive_messages(server_socket, message_queue):
    global addr
    while True:
        # store the message and the address of the sender
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()
        # if the message is the address collection message, ignore it
        if message == "7jFp$KlQz2E5xP&v1YnR9Gy@U0W#oAqBcZrD8sIt6Xw3VhLmN4eSfTgOuHbMaCi":
            pass
        # else print the message and ask for a reply
        else:
            message_queue.put(("U1", message))
            print("\rU1:", message)
            print("U2:", end=" ", flush=True)  # Print U2: without a newline

            if message.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                os._exit(2)

# Function to send messages
def send_messages(server_socket, message_queue):
    global addr
    while True:
        # get the reply and send it to the address of the sender
        reply = input("U2: ")
        server_socket.sendto(reply.encode(), addr)
        message_queue.put(("U2", reply))
        # print("\rU2:", reply)  # Overwrite the previous U2: message
        # print("\033[KU2:", end=" ", flush=True)  # Clears the line after U2:

        if reply.lower() in ["exit", "quit"]:
            print("Ending conversation...")
            os._exit(1)

# Main function
def main():
    # Check if the command line arguments are valid
    if len(sys.argv) != 3 or sys.argv[1] != "-p":
        print("Usage: python3 u2.py -p <port>")
        sys.exit(0)

    # Get the port number from command line arguments
    port = int(sys.argv[2])

    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", port))

    # print("Host: ", socket.gethostbyname(socket.gethostname()))
    print("U2 is waiting for connections on port", port)

    # Create a queue to store messages
    message_queue = queue.Queue()

    # Start threads for sending and receiving messages
    sending_thread = threading.Thread(target=send_messages, args=(server_socket, message_queue))
    receiving_thread = threading.Thread(target=receive_messages, args=(server_socket, message_queue))

    sending_thread.start()
    receiving_thread.start()          

if __name__ == "__main__":
    main()