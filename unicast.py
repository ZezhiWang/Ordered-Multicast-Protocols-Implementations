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
    pid = sys.argv[1]
    #get the ip address and port number of config file
    host, port = config_map[destination]
    #connect to host/port
    send_socket.connect((host, port))

    #send the message
    send_socket.send(pid + "," + message)

def unicast_receive(source, message):
	print "Process" + source + ": " + message

def socket_listen_thread():
	sock.listen(5)
	print "Socket now listening..."

	while True:
		conn, address = sock.accept()

		ip, port = str(address[0]), int(address[1])
		pid, message = conn.recv(1024).split(",", 1)
		unicast_receive(pid, message)
		conn.close()


def main():
	parse_config("config.txt")
	pid = sys.argv[1]
	sock.bind((config_map[pid][0], config_map[pid][1]))

	Thread(target=socket_listen_thread).start()

	while True:
		command, dest, message = raw_input().split(" ", 2)
		if command == "send":
			unicast_send(dest, message)

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	main()


