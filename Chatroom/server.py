import socket
import select

HEADER_LENGTH = 10
#IP = "127.0.0.1"
IP = "192.168.1.6"
#IP = "0.0.0.0"
#IP = ""
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))

server_socket.listen(5)

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notifiend_socket in read_sockets:
        if notifiend_socket == server_socket:
            client_socket, client_adress = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"{user['data'].decode('utf-8')} joined the chat from ip: {client_adress[0]} and port {client_adress[1]}")

            head = "server".encode('utf-8')
            head_header = f"{len(head):<{HEADER_LENGTH}}".encode('utf-8')
            msg = f"{user['data'].decode('utf-8')} joined the chat".encode('utf-8')
            msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
            for client_socket in clients:
                if client_socket != notifiend_socket:
                    client_socket.send(head_header + head + msg_header + msg)

        else:
            message = receive_message(notifiend_socket)
            if message is False:
                print(f"Closed connection from {clients[notifiend_socket]['data'].decode('utf-8')}")

                #msg = f"{clients[notifiend_socket]['data'].decode('utf-8')} has left the chat".encode('utf-8')
                #msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                #for client_socket in clients:
                #    if client_socket != notifiend_socket:
                #        client_socket.send(msg_header + msg)

                head = "server".encode('utf-8')
                head_header = f"{len(head):<{HEADER_LENGTH}}".encode('utf-8')
                msg = f"{clients[notifiend_socket]['data'].decode('utf-8')} has left the chat".encode('utf-8')
                msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
                for client_socket in clients:
                    if client_socket != notifiend_socket:
                        client_socket.send(head_header + head + msg_header + msg)

                sockets_list.remove(notifiend_socket)
                del clients[notifiend_socket]

                continue
            user = clients[notifiend_socket]
            print(f"received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                if client_socket != notifiend_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notifiend_socket in exception_sockets:
        sockets_list.remove(notifiend_socket)
        del clients[notifiend_socket]
