import socket
import os
import threading

running = True

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024*4


client_ip = None
#host = "192.168.1.6"
host = "223.184.73.118"

def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    #progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transmission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            #progress.update(len(bytes_read))

    # close the socket
    s.close()
    print("                                     message sent")


def receive_file():
    global client_ip
    # device's IP address
    SERVER_HOST = socket.gethostname()
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"
    # create the server socket
    # TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))
    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(20)
    #print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    # accept connection if there is any
    client_socket, address = s.accept()
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = "received_data.bin"
    # convert to integer
    filesize = int(filesize)
    # start receiving the file from the socket
    # and writing to the file stream
    # progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            # progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()
    client_ip = address[0]


def look_for_messages():
    global running
    global client_ip
    global host
    while running:
        receive_file()
        file = open("received_data.bin", "rb+")
        print(str(file.read())[2:-1])
        file.close()
        host = client_ip



    """
    import argparse
    parser = argparse.ArgumentParser(description="Simple File Sender")
    parser.add_argument("file", help="File name to send")
    parser.add_argument("host", help="The host/IP address of the receiver")
    parser.add_argument("-p", "--port", help="Port to use, default is 5001", default=5001)
    args = parser.parse_args()
    """
filename = "data_file.bin"
port = 5001
receiver = threading.Thread(target=look_for_messages)
receiver.start()
while running:
    text = input(" ")
    if text == "EXIT":
        running = False
        break
    file = open("data_file.bin", "wb")
    file.write(text.encode())
    file.close()
    send_file(filename, host, port)
        #sender = threading.Thread(target=send_file, args=(filename, host, port))
        #sender.start()
receiver.join()

