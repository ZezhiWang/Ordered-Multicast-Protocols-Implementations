import socket
import sys
import traceback
from threading import Thread
import time
from random import *

def parse_config(filename):
	config = open(filename, "r")
	tmpMap, tmpInv = {}, {}
	for line in config:
		lineList = line.split()
		tmpMap[lineList[0]] = (lineList[1], int(lineList[2]))
		tmpInv[(lineList[1], int(lineList[2]))] = lineList[0]
	return tmpMap, tmpInv

config_map, config_inv = parse_config("config.txt")


def delay_send(destination, message):
	#minTime, maxTime = config_map 

	minTime = 1
	maxTime = 3
	delay_time = randint(minTime, maxTime)
	Thread(target=unicast_send, args=(destination, message, delay_time)).start()
	

def unicast_send(destination, message, delay_time):
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	pid = sys.argv[1]

	print "Sent " + message + "to process "+ destination + "with system time: " + str(time.time())
	time.sleep(delay_time)
	#get the ip address and port number of config file
	host, port = config_map[destination]
	#connect to host/port
	send_socket.connect((host, port))	
	#send the message
	send_socket.send(pid + "," + message)	
	send_socket.close()
    

def unicast_receive(source, message):
	print "Received" + message + "from process" + source + "with system time is" + str(time.time())

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
	pid = sys.argv[1]
	sock.bind((config_map[pid][0], config_map[pid][1]))

	Thread(target=socket_listen_thread).start()

	while True:
		command, dest, message = raw_input().split(" ", 2)
			delay_send(dest, message)

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	main()
