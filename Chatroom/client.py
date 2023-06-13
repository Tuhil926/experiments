import socket
import select
import errno
import sys
import threading
import time

HEADER_LENGTH = 10

IP = "192.168.1.12"
#print(socket.gethostbyname(socket.gethostname()))
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((IP, PORT))
except Exception as e:
    print(str(e))
    time.sleep(3)
    sys.exit()
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

message = ""
msg_thread = None


def get_input():
    global message
    global msg_thread
    message = input("")
    msg_thread = None


while True:
    #message = input(f"{my_username}: ")
    if msg_thread is None:
        msg_thread = threading.Thread(None, get_input)
        msg_thread.start()

    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        message = ""
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8"))
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username}: {message}")
            message = ""

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print("General error: ", str(e))
        sys.exit()
