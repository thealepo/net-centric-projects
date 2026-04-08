import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def start_server():
    print("Starting server...")

    # RSA stuff
    print("Creating RSA keypair")
    # create keypair
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048
    )

    public_key = private_key.public_key()

    # serialize keypair for transmission
    serialized_private_key = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

    serialized_public_key = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print("RSA keypair created")

    print("Creating server socket")
    # control socket on port 8080
    control_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    control_socket.bind(('localhost' , 8080))
    control_socket.listen(1)

    print("Awaiting connections...")
    connection , address = control_socket.accept()

    command = connection.recv(1024).decode('utf-8')
    
    if command == 'connect':
        print("Connection requested. Creating data socket")
        # setting up new data socket
        data_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        data_socket.bind(('localhost' , 0))
        data_socket.listen(1)

        data_port = data_socket.getsockname()[1]
        connection.send(str(data_port).encode('utf-8'))

        data_connection , data_address = data_socket.accept()
        command = data_connection.recv(1024).decode('utf-8')

    if command == 'tunnel':
        print("Tunnel requested. Sending public key")

        data_connection.send(serialized_public_key)

        message = data_connection.recv(1024).decode()
        # remove message header and footer
        message = message[26: -25]


    print("Post requested.")

    #print(f"Decrypted message: {encrypted_message}")

    print("Computing hash")

    #print(f"Responding with hash: {message_hash}")

if __name__ == "__main__":
    start_server()