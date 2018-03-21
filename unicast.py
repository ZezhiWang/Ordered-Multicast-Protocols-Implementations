'''
	Implementation of unicast functionalities with TCP
	
	Authors: Zezhi (Herry) Wang, Yajie (Angus) Zhao, Shikun (Jason) Wang
	Date: Mar 17, 2018
''' 
import socket #socket programming
import sys
from threading import Thread, Lock #multithreading
import time
from random import *
import pickle	#data serialization

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
	for line in lines:
		lineList = line.split()
		tmpMap[lineList[0]] = (lineList[1], int(lineList[2]))
		tmpInv[(lineList[1], int(lineList[2]))] = lineList[0]
	return minTime, maxTime, tmpMap, tmpInv

#initial delay range and config map
delay_range = [0,0]
delay_range[0], delay_range[1], config_map, config_inv = parse_config("config.txt")

class Unicast:
	'''
	Implementation of Unicast Functionalities, send and receive
	
	Attributes:
		config_map(dict): id(str) -> ip(str), port(int)
		max_number(int): capacity of the network
		delay_range(list): [0] is min delay, [1] is max delay
		strategy(func): the stragey for order. Default unicaste_received
	'''
	def unicast_receive(source, message):
		'''unicast deliver, and print out the message

		Args:
			source(str): deliver message sent from source
			message(str): message that needs to be deliver
		'''
		if message['msg'] == 'bye':
			print "Listener stopped, press ENTER to exit."
			return True
		print "Received \"%s\" from process %s with system time: %f s" % (message['msg'], source, time.time())
		return False

	def __init__(self, pid, max_number, delay_range, strategy=unicast_receive, config_map = config_map, config_inv = config_inv):
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
		# init mutex lock
		self.lock = Lock()
		#random seed for testing, each node has different seed
		self.random_seed = [x for x in range(max_number)]
		seed(self.random_seed[int(self.pid)]) 
		#Spawn a thread for listening msg from other nodes
		Thread(target=self.socket_listen_thread, args=(strategy,)).start()

	def isRunning(self):
		'''detect if the node is running'''
		return self.running

	def socket_listen_thread(self, strategy):
		'''Put each running nodes constanting waiting for others message

		Args:
			strategy(func): fifo, total, casual ordering
		'''
		#create a listening socket
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as err:
			print "socket creation failed with error"
			sys.exit(1)
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
			try:
				pid, message = conn.recv(1024).split(",", 1)
			except socket.error, e:
				print "Error receiving data"

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
		print "\tSent \"%s\" to process %s with system time: %f s" % (message['msg'], destination, time.time())
		data = pickle.dumps(message) #serialized the message
		Thread(target=self.delay_send, args=(destination, data, delay_time)).start()

	def delay_send(self, destination, message, delay_time):
		'''function that used to send message with TCP

		Args:
			destination: id number of the node
			message: message that we send
			delay_time: simulated network delay

		'''
		time.sleep(delay_time) #network delay

		host, port = self.config_map[destination]
		self.lock.acquire()
		#send message
		try:
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			send_socket.connect((host, port)) #connect to host/port and send
			send_socket.send(self.pid + "," + message)
			send_socket.close() # closed the socket when finish
		except socket.error, e:
			print '\tListener already down.'
		except socket.gaierror, e:
			print '\tNothing is wrong.'
		self.lock.release()

#testing unicast  
def main():
	pid = sys.argv[1]
	unicast_node = Unicast(pid, 5, delay_range)	
	while True:
		user_input = raw_input()
		if not unicast_node.isRunning():
			break
		_, dest, message = user_input.split(" ", 2)
		unicast_node.unicast_send(dest, {'msg':message})

if __name__ == "__main__":
	main()