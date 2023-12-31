# UDP Talk Application

This is a simple UDP-based chat program implemented in Python. It allows two users to exchange messages over a network connection. The program consists of two scripts, `u1.py` and `u2.py`, each representing one side of the chat.

## Directory Structure

The project directory is organized as follows:

- `u1.py`: This script represents one user and allows them to send and receive messages.
- `u2.py`: This script represents the other user and also allows them to send and receive messages.
- `readme.md`: This README file providing information about the project.
- `script.sh`: A script file that contains instructions on how to run the code.

## Function of Each File

- `u1.py`:
  - Imports necessary libraries and modules.
  - Defines functions for sending and receiving messages.
  - Uses multi-threading to handle message sending and receiving concurrently.
  - Reads command-line arguments to specify the server IP and port.
  - Creates a UDP socket, connects to the server, and starts communication.

- `u2.py`:
  - Imports necessary libraries and modules.
  - Defines functions for sending and receiving messages.
  - Uses multi-threading to handle message sending and receiving concurrently.
  - Binds to a specific port and waits for incoming connections.
  - Once connected, it communicates with the user represented by `u1.py`.

## How to Run

To run the chat program, follow these steps:

1. Open two terminal windows or command prompts.

2. In the first window, navigate to the project directory and run the server side `u2.py` script with the following command first, specifying the port to listen on as an argument:

```
python3 u2.py -p <port>
```

2. In the second window, navigate to the project directory and run the client side `u1.py` script with the following command after server side is running, specifying the server IP and port as arguments:

```
python3 u1.py -s <server_ip> -p <server_port>
```

4. You can now start exchanging messages between the two users by typing messages in the respective terminal windows. To exit the chat program, type "exit" or "quit."

- Link to the demo video : https://drive.google.com/drive/folders/1WS2drjrHP3KqhyiyAzjv1aLZMuqsX2Pm?usp=drive_link