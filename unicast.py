import socket
import sys
import traceback
from threading import Thread

config_map = {}
config_inv = {}

def parse_config(filename):
	config = open(filename, "r")
	for line in config:
		lineList = line.split()
		config_map[lineList[0]] = (lineList[1], int(lineList[2]))
		config_inv[(lineList[1], int(lineList[2]))] = lineList[0]

def unicast_send(destination, message):
    #get the ip address and port number of config file
    print config_map[destination]
    host, port = config_map[destination]
    print host, port
    #connect to host/port
    sock.connect((host, port))

    #send the message
    sock.send(message)

def unicast_receive(source, message):
	print "Process" + source + ": " + message

def socket_listen_thread():
	sock.listen(5)
	print "Socket now listening..."

	while True:
		conn, address = sock.accept()
		print "accept"

		ip, port = str(address[0]), int(address[1])
		message = conn.recv(1024)
		unicast_receive(config_inv(ip, port), message)
		conn.close()


def main():
	parse_config("config.txt")
	id = sys.argv[1]
	sock.bind((config_map[id][0], config_map[id][1]))

	Thread(target=socket_listen_thread).start()

	while True:
		command, dest, message = raw_input().split(" ", 2)
		if command == "send":
			unicast_send(dest, message)

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main()


