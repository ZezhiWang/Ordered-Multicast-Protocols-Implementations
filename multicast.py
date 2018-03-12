import unicast
import time
from threading import Thread

orderTypes = [fifo, total, causal]
orderRecv = [fifoRecv, totalRecv, causalRecv]

_, _, config_map, config_inv = unicast.parse_config("config.txt")
sock = unicast.sock
send_socket = unicast.send_socket

def Main():
	funcId = sys.argv[1]
	mult = orderTypes[funcId]
	recv = orderRecv[funcId]

	sock.bind((config_map[pid][0], config_map[pid][1]))
	Thread(target = recv).start()

	while True:
		_,msg = raw_input().split(" ",1)
		mult(msg)

def basic(msg):
	for idx in config_map.keys:
		unicast.unicast_send(idx, msg)

def fifo(msg):
	# num of msg cur server has sent to group
	S = 0
	# seq num of latest group msg cur server has delievered from other server
	global R = [0 for i in range(len(config_map.keys))]
	for key in config_map.keys:
		R[key] = 0
	# increment S by 1
	S += 1
	# piggy back S into msg
	val = str(S) + "," + msg
	# B-multicast
	basic(val)

def fifoRecv():
	def helper(sender, seq, val):
		# if S = R[q] + 1
		if seq == R[sender] + 1:
			# Fifo deliever msg
			deliever(sender, msg)
			# increment R[q]
			R[sender] += 1
			# check msg in hold-back queue
			for val in queue:
				seq,sender,msg = val
				if seq == R[sender] + 1:
					deliever(msg)
					R[sender] += 1
		# if S > R[q]
		elif seq > R[sender] + 1:
			# put msg in hold-back queue
			queue.append((seq,sender,msg))
		# else reject
		return
	# init hold-back queue
	queue = []
	# init sock to listen
	sock.listen(5)
	while True:
		conn,_ = sock.accept()
		# split senderID and seq and msg from val
		sender, seq, val = conn.recv(1024).split(",", 2)
		helper(sender, seq, val)

def total(msg):

def totalRecv():

def causal(msg):
	# vector timestamp init
	global V = [0 for idx in len(config_map.keys)]
	# increment V[i] by 1
	V[ID] += 1
	# piggy back vector timestamp

	# basic mult
	basic(msg)

def causalRecv():
	def helper(sender, vec, val):
		# place val in hold-back queue
		queue.insert(0,(sender, vec, msg))
		# loop through queue
		for val in queue:
			sender, vec, msg = val
			if vec[sender] = V[sender] + 1:
				flag = True
				for idx in xrange(len(V)):
					if vec[idx] > V[idx]:
						flag = False
				if flag:
					deliever(sender, msg)
		return
	# init hold-back queue
	queue = []
	# init sock to listen
	sock.listen(5)
	while True:
		conn,_ = sock.accept()
		# split senderID time, and msg from val
		sender, vec, msg = conn.recv(1024).split(",", 2)
		helper(sender, vec, val)

def deliever(sender, msg):
	print sender, time.time(), msg

if __name__ == "__main__":
	Main()