import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def start_client():
    print("Starting client...")

    
    print("Creating RSA keypair")
    private_key = rsa.generate_private_key(
        public_exponent = 65537,
        key_size = 2048
    )

    public_key = private_key.public_key()

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
    data_socket.send(b'tunnel')

    print("Server public key received")
    response = data_socket.recv(1024).decode('utf-8')
    
    # remove message header and footer
    server_key = response[26: -25]

    print("Tunnel established")
    data_socket.send(serialized_public_key)

    print("Encrypting message: Hello")

    #print(f"Sending encrypted message: {encrypted_message}")

    print("Received hash")
    print("Computing hash")
    print("Secure")

if __name__ == "__main__":
    start_client()