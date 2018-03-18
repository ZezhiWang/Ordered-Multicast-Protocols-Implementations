'''Implementation of unicast functionalities with TCP
	Author: Zezhi (Harry) Wang, Yajie (Angus) Zhao, Shikun (Jason) Wang
''' 
import socket #socket programming
import sys
import traceback
from threading import Thread #multithreading
import time
from random import *
import pickle	#data serialization

#config map  str(id) -> str(ip), int(port)
#config inv   str(ip), int -> str(id_
def parse_config(filename):
	'''parse configuration file to a hash map

	Args:
		filename: the name of configuration file

	return:
		config map: str(id) -> str(ip), int(port)
		config inv: str(ip), int(port) -> str(id)
	'''
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

#testing
#delay_range = [0,0]
#delay_range[0], delay_range[1], config_map, config_inv = parse_config("config.txt")

class Unicast:
	'''
	Implementation of Unicast Functionalities, send and receive
	
	Attributes:
		config_map(dict): id(str) -> ip(str), port(int)
		max_number(int): capacity of the network
		delay_range(list): [0] is min delay, [1] is max delay
		strategy(func): the stragey for order. Default unicaste_received
	'''
	def __init__(self, pid, max_number, delay_range, strategy=unicast_receive, config_map = config_map, config_inv = config_inv, ):
		'''
		Initialization of the object

		Args:
			config_map(dict): id(str) -> ip(str), port(int)
			max_number(int): capacity of the network
			delay_range(list): [0] is min delay, [1] is max delay
			strategy(func): the stragey for order. Default unicaste_received
		'''
		self.config_map = config_map
		self.max_nodes = max_number
		self.delay_range = delay_range
		self.config_inv = config_inv
		self.pid = pid
		self.running = True
		#Spawn a thread for listening msg from other nodes
		Thread(target=self.socket_listen_thread, args=(strategy,)).start()


	def isRunning(self):
		'''detect if the node is running'''
		return self.running


	def unicast_receive(self, source, message):
		'''unicast deliver, and print out the message

		Args:
			source(str): deliver message sent from source
			message(str): message that needs to be deliver
		'''
		print "Received " + message + " from process " + source + " with system time is " + str(time.time())
		return message == 'bye'

	def socket_listen_thread(self, strategy):
		'''Put each running nodes constanting waiting for others message

		Args:
			strategy(func): fifo, total, casual ordering
		'''

		#create a listening socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#bind socket to the corresponding port number and id number
		sock.bind((self.config_map[self.pid][0], self.config_map[self.pid][1]))
		#set maximum number of nodes 
		sock.listen(self.max_nodes)

		#listening
		while True:
			#connect with a nodes when receive a request
			conn, address = sock.accept()
			#get the ip address and port number of the sender
			ip, port = str(address[0]), int(address[1])
			#decode the message received
			pid, message = conn.recv(1024).split(",", 1)
			data_received = pickle.loads(message)
			#use particular ordering the deliver
			flag = strategy(pid, data_received)
			#close connection
			conn.close()
			#check exit signal
			if flag:
				self.running = False
				break

	def unicast_send(self, destination, message):
		''' unicast send implementation with network delay

		Args:
			destination(str): the id number of the node of destination
			message(str): message that we want to sent
		'''

		#get the random number of delay range as our network delay
		delay_time = uniform(self.delay_range[0], self.delay_range[1])
		#create a thread to send the message
		Thread(target=self.delay_send, args=(destination, message, delay_time)).start()


	def delay_send(self, destination, message, delay_time):
		'''function that used to send message with TCP

		Args:
			destination: id number of the node
			message: message that we send
			delay_time: simulated network delay

		'''

		#send message
		send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pid = sys.argv[1] # get id from user input

		print "    Sent " + message['msg'] + " to process "+ destination + " with system time: " + str(time.time())
		host, port = self.config_map[destination]
		data = pickle.dumps(message) #serialized the message
		time.sleep(delay_time) #network delay
		send_socket.connect((host, port)) #connect to host/port and send
		send_socket.send(pid + "," + data)
		send_socket.close() # closed the socket when finish


#testing 
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
