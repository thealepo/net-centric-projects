# Help: https://www.eventhelix.com/networking/ftp/
# Help: https://www.eventhelix.com/networking/ftp/FTP_Port_21.pdf
# Help: https://realpython.com/python-sockets/
# Help: PASV mode may be easier in the long run. Active mode works 
# Reading: https://unix.stackexchange.com/questions/93566/ls-command-in-ftp-not-working
# Reading: https://stackoverflow.com/questions/14498331/what-should-be-the-ftp-response-to-pasv-command

#Alex Sanchez PID:6403828
#Curt Francis PID:6328922
#Deryn Hurst PID:6457077

#import socket module
from socket import *
import sys # In order to terminate the program

def quitFTP(clientSocket):
    # COMPLETE
    command = 'QUIT' + '\r\n' # complete the QUIT command
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut)
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    print(data)

def sendCommand(socket, command):
    dataOut = command.encode("utf-8")
    # Complete
    socket.sendall(dataOut)
    dataIn = socket.recv(1024) #receive the data (bytes)
    data = dataIn.decode('utf-8')  #decode thh data to utf-8
    return data #return the data

def receiveData(clientSocket):
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

# If you use passive mode you may want to use this method but you have to complete it
# You will not be penalized if you don't
def modePASV(clientSocket):
    command = "PASV" + "\r\n"
    # Complete
    data = sendCommand(clientSocket , command)
    status = 0
    if data.startswith("227"):
        status = 227
        # Complete
        
        # ip is first 4 numbers, port is last 2 numbers calculated (N5*256)+N6
        # "(222,3,2,321,3,54)"
        # "222,3,2,321,3,54"
        # "[222,3,2,321,3,54]"
        # ip = 22232321
        # port = equation(3,54)
        
        start , end = data.find('(')+1 , data.find(')') #find parenthesis
        content = data[start:end] #make a new string (content between the parenthesis)
        numbers = content.split(',') #split the numbers by the comma
        ip , port = '.'.join(numbers[:4]) , (int(numbers[4])*256)+int(numbers[5]) #grab the frist 4 numbers

        dataSocket = socket(AF_INET , SOCK_STREAM)
        dataSocket.connect((ip, port))
        
    return status, dataSocket

    
    
def main():
    # COMPLETE

    username = input("Enter the username: ")
    password = input("Enter the password: ")

    clientSocket = socket(AF_INET, SOCK_STREAM) # TCP socket initialization
    # COMPLETE
    PORT = 21 #port number (constant for PORT)

    HOST = sys.argv[1] # 2nd parameter command line
    # COMPLETE
    
    clientSocket.connect((HOST, PORT)) # connect the socket to the host and the port

    dataIn = receiveData(clientSocket)
    print(dataIn)

    status = 0
    
    if dataIn.startswith("220"):
        status = 220
        print("Sending username")
        # COMPLETE
        dataIn = sendCommand(clientSocket,"USER "+username+"\r\n") #send username
        print(dataIn)

        print("Sending password")
        if dataIn.startswith("331"):
            status = 331
            # COMPLETE
            dataIn = sendCommand(clientSocket,'PASS '+password+'\r\n') #send password

            print(dataIn)
            if dataIn.startswith("230"):
                status = 230

    
    if status == 230:
        # It is your choice whether to use ACTIVE or PASV mode. In any event:
        # COMPLETE
        pasvStatus, dataSocket = modePASV(clientSocket)
        if pasvStatus == 227:
            # COMPLETE
            while True:
                userInput = input('myftp> ').strip()
                split = userInput.split()
                command , arg = split[0] , split[1] if len(split) > 1 else ''
                  
                if command == 'ls': #show list
                    pasvStatus , dataSocket = modePASV(clientSocket)
                    if pasvStatus == 227 and dataSocket is not None:
                        returnCode = sendCommand(clientSocket, 'LIST\r\n')#passes data
                        print(returnCode)
                        while True:
                            data = dataSocket.recv(1024)
                            if not data:
                                break
                            print(data.decode(), end='')
                        dataSocket.close()
                        print(receiveData(clientSocket))

                elif command == 'cd': #enter remote directory
                    returnCode = sendCommand(clientSocket, 'CWD '+arg+'\r\n') #change working directory

                elif command == 'get': #get the remote file
                    pasvStatus , dataSocket = modePASV(clientSocket) #passes data 
                    if pasvStatus != 227 or dataSocket is None:
                        print("PASV failed")
                        continue
                    returnCode = sendCommand(clientSocket,'RETR '+arg+'\r\n') # retrive file
                    print(returnCode)
                    while True:
                        data = dataSocket.recv(1024)
                        if not data:
                            break
                        print(data.decode(), end='')
                    dataSocket.close()
                    print(receiveData(clientSocket))

                elif command == 'put': #upload file to server
                    pasvStatus , dataSocket = modePASV(clientSocket) #passes data
                    if pasvStatus == 227 and dataSocket is not None:
                        returnCode = sendCommand(clientSocket,'STOR '+arg+'\r\n') #store file 
                        print(returnCode)
                        bytess = open(arg, 'rb') 
                        while True:
                            bytess_data = bytess.read(1024)
                            if not bytess_data:
                                break
                            dataSocket.sendall(bytess_data)#we send the bytes data
                        dataSocket.close() #close the socket 
                        bytess.close()
                        reply = receiveData(clientSocket) #receive the data 
                        print(reply) #print the data we receive

                elif command == 'delete': # delete the remote file
                    returnCode = sendCommand(clientSocket,'DELE '+arg+'\r\n')
                    print(returnCode)
                    
                elif command == 'quit':
                    quitFTP(clientSocket)
                    break                     
                    
    
    print("Disconnecting...")
    
    clientSocket.close()
    dataSocket.close()
    
    sys.exit()#Terminate the program after sending the corresponding data

main()

