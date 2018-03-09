import socket
import sys
import traceback
from threading import Thread
import time

def parse_config(filename):
	config = open(filename, "r")
	tmpMap, tmpInv = {}, {}
	for line in config:
		lineList = line.split()
		tmpMap[lineList[0]] = (lineList[1], int(lineList[2]))
		tmpInv[(lineList[1], int(lineList[2]))] = lineList[0]
	return tmpMap, tmpInv

config_map, config_inv = parse_config("config.txt")

def unicast_send(destination, message):
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pid = sys.argv[1]
	time.sleep(5)
	#get the ip address and port number of config file
	host, port = config_map[destination]
	#connect to host/port
	send_socket.connect((host, port))	
	#send the message
	send_socket.send(pid + "," + message)	
	send_socket.close()
    

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
		print time.time()
		conn.close()

def main():
	pid = sys.argv[1]
	sock.bind((config_map[pid][0], config_map[pid][1]))

	Thread(target=socket_listen_thread).start()

	while True:
		command, dest, message = raw_input().split(" ", 2)
		if command == "send":
			print time.time()
			Thread(target=unicast_send, args=(dest, message)).start()

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	main()
