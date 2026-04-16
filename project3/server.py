import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

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
        client_key = message[26: -25]


    print("Post requested.")

    data_connection.recv(1024)  # consume 'post' command
    encrypted_message = b''
    while len(encrypted_message) < 256:
        chunk = data_connection.recv(256 - len(encrypted_message))
        encrypted_message += chunk
    print(f"Received encrypted message: {encrypted_message.hex()}")

 
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"Decrypted message: {decrypted_message.decode('utf-8')}")

    print("Computing hash")
    import hashlib
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    message_hash = hashlib.sha256(decrypted_message).digest()
    print(f"Responding with hash: {message_hash.hex()}")

    client_public_key = load_pem_public_key(
        b'-----BEGIN PUBLIC KEY-----' + client_key.encode() + b'-----END PUBLIC KEY-----'
    )
    encrypted_hash = client_public_key.encrypt(
        message_hash,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    data_connection.send(encrypted_hash)

    print("Computing hash")

    #print(f"Responding with hash: {message_hash}")

if __name__ == "__main__":
    start_server()

    #print(f"Responding with hash: {message_hash}")

if __name__ == "__main__":
    start_server()
