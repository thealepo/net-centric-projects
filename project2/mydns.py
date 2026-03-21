import socket
import sys

def sendQueryToRoot(request):
    # COMPLETE
    hostname = request[0]
    server = request[1]
    print("DNS server to query: " + server)    

    receiveRootReply(hostname, server)
    

def receiveRootReply(hostname, server):
    # COMPLETE
    print()

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