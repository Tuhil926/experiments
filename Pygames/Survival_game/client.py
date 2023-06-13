import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = ""
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"new message length: {msg[:10]}")
            msglen = int(msg[:10])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg) - 10 == msglen:
            print("Full message received")
            print(full_msg[10:])
            new_msg = True
            full_msg = ''
    print(full_msg)