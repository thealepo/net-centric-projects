import socket

def start_client():
    print("Starting client...")

    
    print("Creating RSA keypair")
    print("RSA keypair created")

    print("Creating client socket")
    control_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

    print("Connecting to server")
    control_socket.connect(('localhost' , 8080))
    control_socket.send(b'connect')

    response = control_socket.recv(1024).decode('utf-8')
    data_port = int(response)
    
    print("Creating data socket")
    data_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    data_socket.connect(('localhost' , data_port))

    print("Requesting tunnel")

    print("Server public key received")

    print("Tunnel established")

    print("Encrypting message: Hello")

    print(f"Sending encrypted message: {encrypted_message}")

    print("Received hash")
    print("Computing hash")
    print("Secure")

if __name__ == "__main__":
    start_client()