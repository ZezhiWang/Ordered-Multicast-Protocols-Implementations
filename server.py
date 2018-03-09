import socket
import sys
import traceback
from threading import Thread


def client_thread(conn, ip, port):
    while True:
        data = conn.recv(1024)
        if not data:
            print ('Bye')
        print data
        conn.send("recived")
    conn.close()

def Main():
    start_server()

def start_server():
    host = "127.0.0.1"
    port = 8888         # arbitrary non-privileged port
    #create a socket object
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")

    #bind the socket to a specific ip address and port
    soc.bind((host, port))

    #listen to 5 clients
    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")
    # infinite loop- do not reset for every requests

    while True:

        #get a request from a client
        conn, address = soc.accept()

        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        Thread(target=client_thread, args=(conn, ip, port)).start()
    soc.close()

if __name__ == '__main__':
    Main()
