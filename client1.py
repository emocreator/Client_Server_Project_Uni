import socket
import sys
import threading

def receive_message(s):
    while True:
        data = s.recv(1024).decode("utf-8")
        if not data:
            break
        print("Server: ", data)

def send_message(s):
    while True:
        message = input("You: ")
        s.send(message.encode("utf-8"))
        if message == "exit":
            break

def main():
    host = 'localhost'
    port = 12345
    s = socket.socket()
    s.connect((host, port))
    receive_thread = threading.Thread(target=receive_message, args=(s,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_message, args=(s,))
    send_thread.start()
    receive_thread.join()
    send_thread.join()
    s.close()

if __name__ == "__main__":
    main()
