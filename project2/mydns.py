import socket
import sys
import struct
import random
import io


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
    print("Reply received. Content overview:")
    displayContent(raw_response)

def parse_dns_header(reader):
    items = struct.unpack("!HHHHHH", reader.read(12))

    return{
        "id" : items[0],
        "flags" : items[1],
        "question_count" : items[2],
        "answer_count" : items[3],
        "authority_count" : items[4],
        "additional_count" : items[5]
    }

def parse_dns_question_name(reader):
    question_name_parts = []
    while True:
        length = reader.read(1)
        if not length:
            break
        length = ord(length)

        if length == 0:
            break

        label = reader.read(length).decode('utf-8')
        question_name_parts.append(label)

    return ".".join(question_name_parts)

def parse_dns_question(reader):
    question_name = parse_dns_question_name(reader)
    question_type, question_class = struct.unpack("!HH", reader.read(4))

    return {
        "question_name" : question_name,
        "question_type" : question_type,
        "question_class" : question_class
    }

def displayContent(raw_response):
    # COMPLETE
    reader = io.BytesIO(raw_response)
    header = parse_dns_header(reader)
    question = parse_dns_question(reader)

    print('\t' + str(header.get('answer_count')) + " Answers.")
    print('\t' + str(header.get('authority_count')) + " Intermediate Name Servers.")
    print('\t' + str(header.get('additional_count')) + " Additional Information Records.")
    

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