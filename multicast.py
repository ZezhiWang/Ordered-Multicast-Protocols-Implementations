import unicast
import time
from threading import Thread

orderTypes = [fifo, total, causal]
config_map, config_inv = unicast.parse_config("config.txt")

def main(func):
	mult = orderTypes[func]
	while True:
		_,msg = input().split(" ",1)
		mult(msg)

def basic(msg):
	for server in servers:
		unicast.unicast_send(server, msg)

def fifo(msg):
	# create fifo listener
	Thread(target = fifoRecv).start()
	# num of msg cur server has sent to group
	S = 0
	# seq num of latest group msg cur server has delievered from other server
	R = {}
	for key in config_map.keys:
		R[key] = 0
	# increment S by 1
	S += 1
	# piggy back S into msg
	val = str(S) + " " + msg
	# B-multicast
	basic(val)

def fifoRecv():
	# init hold-back queue
	queue = []
	def helper(sender,msg):
		# if S = R[q] + 1
		if seq == R[sender] + 1:
			# Fifo deliever msg
			deliever(sender, msg)
			# increment R[q]
			R[sender] += 1
			# check msg in hold-back queue
			while not queue:
				if seq == R[sender] + 1:
					deliever(msg)
					R[sender] += 1
				else:
					break
		# if S > R[q]
		elif seq > R[sender] + 1:
			# put msg in hold-back queue
			queue.insert(0,msg)
		# else reject
		return
	while True:
		seq,msg = conn.recv(1024).split(" ",1)
		helper(seq, msg)

def total(msg):

def causal(msg):


def deliever(sender, msg):
	print sender, time.time(), msg
