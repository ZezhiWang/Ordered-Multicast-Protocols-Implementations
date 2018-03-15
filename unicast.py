import socket
import sys
import traceback
from threading import Thread
import time
from random import *
import pickle

#config map  str(id) -> str(ip), int(port)
#config inv   str(ip), int -> str(id_
def parse_config(filename):
	config = open(filename, "r")
	tmpMap, tmpInv = {}, {}
	with open(filename, "r") as config:
		lines = config.read().splitlines()
	line = lines.pop(0).split(" ",1)
	minTime = int(line[0]) / 1000.0
	maxTime = int(line[1]) / 1000.0
	print "test: "
	print minTime, maxTime
	for line in lines:
		lineList = line.split()
		tmpMap[lineList[0]] = (lineList[1], int(lineList[2]))
		tmpInv[(lineList[1], int(lineList[2]))] = lineList[0]
	return minTime, maxTime, tmpMap, tmpInv

delay_range = [0,0]
delay_range[0], delay_range[1], config_map, config_inv = parse_config("config.txt")

class Unicast:
	def unicast_receive(self, source, message):
		print "Received " + message + " from process " + source + " with system time is " + str(time.time())

	#initialized config file and max number of nodes in the system
	def __init__(self, pid, max_number, delay_range, strategy=unicast_receive, config_map = config_map, config_inv = config_inv, ):
		self.config_map = config_map
		self.max_nodes = max_number
		self.delay_range = delay_range
		self.config_inv = config_inv
		self.pid = pid
		Thread(target=self.socket_listen_thread, args=(strategy,)).start()

	#listening from other nodes
	def socket_listen_thread(self, strategy):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((self.config_map[self.pid][0], self.config_map[self.pid][1]))
		sock.listen(self.max_nodes)
		print "Socket now listening..."
		while True:
			conn, address = sock.accept()

			ip, port = str(address[0]), int(address[1])
			pid, message = conn.recv(1024).split(",", 1)
			data_received = pickle.load(message)
			strategy(pid, data_received)
			conn.close()


	def unicast_send(self, destination, message):
		#minTime, maxTime = config_map

		delay_time = uniform(delay_range[0], delay_range[1])
		Thread(target=self.delay_send, args=(destination, message, delay_time)).start()


	def delay_send(self, destination, message, delay_time):
		send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pid = sys.argv[1]

		print "Sent " + message + " to process "+ destination + " with system time: " + str(time.time())
		time.sleep(delay_time)
		#get the ip address and port number of config file
		host, port = self.config_map[destination]
		#connect to host/port
		send_socket.connect((host, port))
		#send the message
		#msg = [1, 2, 3]
		data = pickle.dumps(message)
		send_socket.send(pid + "," + data)
		send_socket.close()


	def unicast_receive(self, source, message):
		print "Received " + message + " from process " + source + " with system time is " + str(time.time())


def main():
	pid = sys.argv[1]
	unicast_node = Unicast(pid, 5, delay_range)	
	while True:
		user_input = raw_input()
		if (user_input == 'bye'):
			break
		command, dest, message = user_input.split(" ", 2)
		if command == "send":
			unicast_node.unicast_send(dest, message)

if __name__ == "__main__":
	main()
