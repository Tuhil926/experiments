import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))

s.listen(5)

while True:
    client_socket, adress = s.accept()
    print(f"Connection from {adress} has been established!")

    msg = "Welcome to the server!"
    msg = f"{len(msg):<10}" + msg

    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(2)
        msg = f"The time is: {time.time()}"
        msg = f"{len(msg):<10}" + msg
        client_socket.send(bytes(msg, "utf-8"))
