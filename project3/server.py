import socket

def start_server():
    print("Starting server...")

    # RSA stuff
    print("Creating RSA keypair")

    print("RSA keypair created")

    print("Creating server socket")
    # control socket on port 8080
    control_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    control_socket.bind(('localhost' , 8080))
    control_socket.listen(1)

    print("Awaiting connections...")
    connection , addrress = control_socket.accept()

    command = connection.recv(1024).decode('utf-8')
    
    if command == 'connect':
        print("Connection requested. Creating data socket")
        # setting up new data socket
        data_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        data_socket.connect(('localhost' , 0))
        data_socket.listen(1)

        data_port = data_socket.getsockname()[1]
        connection.send(str(data_port).encode('utf-8'))

        data_connection , data_address = data_socket.accept()

    print("Tunnel requested. Sending public key")

    print("Post requested.")

    print(f"Decrypted message: {encrypted_message}")

    print("Computing hash")

    print(f"Responding with hash: {message_hash}")

if __name__ == "__main__":
    start_server()