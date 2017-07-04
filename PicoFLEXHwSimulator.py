import socket
import sys
import random

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Then bind() is used to associate the socket with the server address.
#In this case, the address is localhost, referring to the current server, and the port number is 10001.
# Bind the socket to the port
server_address = ('localhost', 10001)
print ("starting up on %s port %s") % server_address
sock.bind(server_address)

#Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    #accept() returns an open connection between the server and client, along with the address of the client.
    #The connection is actually a different socket on another port (assigned by the kernel).
    #Data is read from the connection with recv() and transmitted with sendall().
    #When communication with a client is finished, the connection needs to be cleaned up using close().
    #This example uses a try:finally block to ensure that close() is always called, even in the event of an error.
    try:
        print ("connection from", client_address)

        reply = ""
        command = ""        

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(64)                                                        
            
            if data:
                
                command = data
                                
                print ("\nReceived %s") % data
                
                if command.rstrip() == "CH1RI:?":
                    value = random.uniform(1.0, 3.0)
                    if value > 2.0:
                        reply = "NAK\r\n"
                    else:
                        reply = "CH1RI:"+str(value)+"\r\n"                    

                elif command.rstrip() == "CH2RI:?":
                    value = random.uniform(1.0, 3.0)
                    if value > 2.0:
                        reply = "NAK\r\n"
                    else:
                        reply = "CH2RI:"+str(value)+"\r\n"  
                elif command.rstrip() == "VER:?":
                    reply = "VER:1.2.4\r\n"

                #Eventually send reply to client device
                connection.sendall(reply)

            else:
                print ("no more data from", client_address)
                break
                
    finally:
        # Clean up the connection
        connection.close()    

