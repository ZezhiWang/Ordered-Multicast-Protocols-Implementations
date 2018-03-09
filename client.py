import socket
import sys


def Main():
    #TCP/IP4
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8881
    soc.connect((host, port))

    print("Enter 'quit' to exit")
    message = "Hello World" 
    while True:

        soc.send(message.encode('ascii'))

        data = soc.recv(1024)

        print('Received from the server :',str(data.decode('ascii')))

        ans = input('\nDo you want to continue(y/n) :')

        if ans == 'y':
            continue
        else:
            break
    soc.close()


if __name__ == "__main__":
    Main()
