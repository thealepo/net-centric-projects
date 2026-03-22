import socket
import sys
import struct
import random
import io
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
    raw_response = receiveRootReply(server, query)
    return raw_response

def receiveRootReply(server, query) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(query, (server, 53))        
        raw_response, _ = sock.recvfrom(4096)
    print("Reply received.")
    return raw_response


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
def parse_rr(reader, data):
    name = read_name(reader, data)
    rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", reader.read(10))
    rdata = reader.read(rdlength)

    return {
        "name": name,
        "type": rtype,
        "class": rclass,
        "ttl": ttl,
        "rdata": rdata
    }

def read_name(reader, data):
    labels = []
    while True:
        length = reader.read(1)[0]

        # pointer (11xxxxxx)
        if (length & 0xC0) == 0xC0:
            pointer_byte = reader.read(1)[0]
            offset = ((length & 0x3F) << 8) | pointer_byte

            current_pos = reader.tell()
            reader.seek(offset)
            labels.append(read_name(reader, data))
            reader.seek(current_pos)
            break

        if length == 0:
            break

        labels.append(reader.read(length).decode())

    return ".".join(labels)

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
    reader = io.BytesIO(raw_response)
    header = parse_dns_header(reader)
    question = parse_dns_question(reader)

    print('\t' + str(header.get('answer_count')) + " Answers.")
    print('\t' + str(header.get('authority_count')) + " Intermediate Name Servers.")
    print('\t' + str(header.get('additional_count')) + " Additional Information Records.")

def extractIP(raw_response):
    reader = io.BytesIO(raw_response)
    header = parse_dns_header(reader)

    # skip question
    for _ in range(header["question_count"]):
        parse_dns_question(reader)

    # skip answers
    for _ in range(header["answer_count"]):
        parse_rr(reader, raw_response)

    # skip authority (NS records)
    for _ in range(header["authority_count"]):
        parse_rr(reader, raw_response)

    # parse additional records with the IPs
    ips = []

    for _ in range(header["additional_count"]):
        rr = parse_rr(reader, raw_response)

        # Type A (IPv4)
        if rr["type"] == 1:
            ip = socket.inet_ntoa(rr["rdata"])
            ips.append(ip)

        # Type AAAA (IPv6)
        elif rr["type"] == 28:
            ip = socket.inet_ntop(socket.AF_INET6, rr["rdata"])
            ips.append(ip)

    return ips

def sendQueryToIntermediate(hostname , intermediate_ip):
    # COMPLETE
    print("DNS server to query: " + intermediate_ip)

    query = build_dns_query(hostname)

    raw_response = receiveIntermediateReply(intermediate_ip , query)
    return raw_response

def receiveIntermediateReply(server_ip , query):
    # COMPLETE
    with socket.socket(socket.AF_INET , socket.SOCK_DGRAM) as sock:
        sock.settimeout(5)
        sock.sendto(query , (server_ip,53))
        raw_response , _ = sock.recvfrom(4096)

    return raw_response

def displayIPs(ips):
    # COMPLETE
    for ip in ips:
        print(ip)


def main():
    request = sys.argv[1:]
    print()
    print("------------------------------------")
    # For main DNS server
    message = sendQueryToRoot(request)
    displayContent(message)
    ips = extractIP(message)
    print("\nIntermediate Name Server IPs:")
    displayIPs(ips)

    # For Intermediate Servers
    r = random.randrange(0,len(ips))
    message = sendQueryToIntermediate(request[0], ips[r])
    print("\nIntermediate response:")
    displayContent(message)

    #For intermediate servers, extract IPs and display
    ips = extractIP(message)
    displayIPs(ips)
main()
