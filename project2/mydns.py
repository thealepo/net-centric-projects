import socket
import sys
import struct
import random


def build_dns_query(domain: str) -> bytes:
    transaction_id = random.randint(0, 65535)
    flags = 0x0100
    header = struct.pack(">HHHHHH", transaction_id, flags, 1, 0, 0, 0)
    question = b""
    for label in domain.rstrip(".").split("."):
        question += bytes([len(label)]) + label.encode()
    question += b"\x00"
    question += struct.pack(">HH", 1, 1)
    return header + question


def sendQueryToRoot(request):
    hostname = request[0]
    server   = request[1]
    print("DNS server to query: " + server)
    query = build_dns_query(hostname)
    receiveRootReply(server, query)


def receiveRootReply(server, query) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(query, (server, 53))        
        raw_response, _ = sock.recvfrom(4096)
    print("Reply received.")
    return raw_response


def displayContent():
    # COMPLETE
    print()

def extractIP():
    # COMPLETE
    print()

def sendQueryToIntermediate():
    # COMPLETE
    print()

def receiveIntermediateReply():
    # COMPLETE
    print()

def displayIPs():
    # COMPLETE
    print()


def main():
    request = sys.argv[1:]
    print()
    print("------------------------------------")
    sendQueryToRoot(request)

main()
