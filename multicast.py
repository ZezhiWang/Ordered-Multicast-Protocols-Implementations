import unicast
import time
from threading import Thread

inits = [fifoInit, totalInit, causalInit]
orders = [fifo, total, causal]
recvs = [fifoRecv, totalRecv, causalRecv]

_, _, config_map, config_inv = unicast.parse_config("config.txt")

# hold-back queue
hbQueue = []

def Main():
	order, maxServer = sys.argv[1:3]
	# init node
	inits[order]()
	global node = unicast.Unicast(config_map, maxServer, delay_range, config_inv, recvs[order])
	
	while True:
		_,msg = raw_input().split(" ",1)
		orders[order](msg)

def basic(msg):
	for idx in config_map.keys:
		node.unicast_send(idx, msg)

def fifoInit():
	# num of msg cur server has sent to group
	global S_fifo = 0
	# seq num of latest group msg cur server has delievered from other server
	global R_fifo = [0 for i in range(len(config_map.keys))]

def fifo(msg):
	# increment S by 1
	S_fifo += 1
	# piggy back S into msg
	val = str(S_fifo) + "," + msg
	# B-multicast
	basic(val)

def fifoRecv(pid, msg):
	def helper(sender, seq, msg):
		# if S = R[q] + 1
		if seq == R_fifo[sender] + 1:
			# Fifo deliever msg
			deliever(sender, msg)
			# increment R[q]
			R[sender] += 1
		# if S > R[q]
		elif seq > R_fifo[sender] + 1:
			# put msg in hold-back queue
			hbQueue.append((sender,seq,msg))
		# check msg in hold-back queue
		for val in hbQueue:
			sender,seq,msg = val
			if seq == R_fifo[sender] + 1:
				hbQueue.remove(val)
				deliever(sender, msg)
				R_fifo[sender] += 1
		# else reject
		return
	# init hold-back queue
	seq, val = conn.recv(1024).split(",", 1)
	helper(int(pid), seq, val)

def totalInit():
	if ID == 0:
		# init sequencer
		global S_total = 0
	else:
		# init group member
		global R_total = 0

def total(msg):
	# piggyback flag
	msg = "mem," + str(R_total) + msg
	# basic multicast msg
	basic(msg)

def totalRecv(pid,msg):
	def helper(seq, pid):
		for val in hbQueue:
			sender, seqTmp, msg = val
			if seqTmp == seq:
				hbQueue.remove(val)
				deliever(sender, msg)
	if ID == 0:
		totalSeqRecv(pid)
	else:
		# split senderID and seq and msg from val
		flag, val = msg.split(",", 1)
		if flag == "mem":
			seq, msg = val.split(",",1)
			hbQueue.append((pid, int(seq), msg))
		else:
			seq, pid = val.split(",",1)
			helper(int(seq), pid)

def totalSeqRecv(pid):
	if pid != str(ID):
		# construct msg
		msg = "order," + str(S_total) + pid
		# basic multicast msg
		basic(msg)
		# increment S_Total
		S_total += 1

def causalInit():
	# vector timestamp init
	global V = [0 for idx in len(config_map.keys)]
	# strat listener
	Thread(target = causalRecv).start()

def causal(msg):
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