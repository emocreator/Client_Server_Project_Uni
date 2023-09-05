# Client_Server_Project_Uni

## Socket Programming Chat Application

This is a simple chat application using socket programming in Python. It consists of a server and client that can communicate with each other.

## Files

It contains the following files:

- server.py - The server code
- client1.py - The client code

## Server

Key features:

- Creates a socket and binds it to localhost and port 12345
- Listens for incoming connections in a loop
- For each client, creates a thread to handle sending and receiving of messages
- Maintains a dictionary of client connections
- Broadcasts messages from one client to all other connected clients
- Closes client sockets gracefully on disconnect

## Client

Key features:

- Creates a socket and connects to the server
- Sends messages to the server by taking user input
- Receives messages from the server and prints them
- Cleanly closes socket on exiting

## Usage

To run the application:

1. Start the server: `python server.py`

To start the server:

```python
python server.py
``` 

This will start the server on localhost port 12345.

2. Open another terminal and run the client: `python client1.py`

To start the client:

```python
python client.py
```

This will connect the client to the running server.

Multiple clients can connect to the same server. Each client connection will be handled in a separate thread.

3. Send messages from the client and observe the communication.
4. Type 'exit' on the client to disconnect gracefully.

## Server

The server has the following capabilities:

- Accept connections from multiple clients
- Receive and send messages to each connected client
- Broadcast messages from one client to all others
- Gracefully handle client disconnections

The main components are:

- Socket creation and binding 
- Listening for connections in a loop
- Spawning a thread per client to handle all communication
- Cleaning up threads when clients disconnect

## Client

The client can:

- Connect to the server 
- Send messages to the server
- Receive messages from the server
- Gracefully handle disconnection

The key components are:

- Socket creation and connection
- Threads for sending and receiving messages
- Clean shutdown on disconnect

## Message Handling

Some of the key aspects of message handling are:

- Prefixing messages with client name
- Detecting client disconnects by empty recv
- Broadcast by looping through all connected clients

## Communication Logic

- The server handles each client connection in a separate thread. 
- When a client sends a message, it is broadcast to all other clients.
- The main threads handle sending and receiving messages independently.

This allows building a simple chat application using socket programming concepts.

Let me know if you would like me to explain or expand any part of the README!

This provides a basic template for building more complex chat applications.
