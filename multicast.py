import unicast
import time
import sys
from threading import Thread

mintime, maxtime, config_map, config_inv = unicast.parse_config("config.txt")
delay_range = [mintime, maxtime]
# hold-back queue
hbQueue = []

def basic(msg):
	for idx in config_map.keys:
		node.unicast_send(idx, msg)

def fifoInit():
	# num of msg cur server has sent to group
	global S_fifo
	S_fifo = 0
	# seq num of latest group msg cur server has delievered from other server
	global R_fifo
	R_fifo = [0 for i in range(len(config_map.keys()))]

def fifo(msg):
	# increment S by 1
	S_fifo += 1
	# piggy back S into msg
	val = {'seq':S_fifo, 'msg':msg}
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
	seq, val = msg.values
	helper(int(pid), seq, val)

def totalInit():
	if ID == 0:
		# init sequencer
		global S_total
		S_total = 0
	else:
		# init group member
		global R_total
		R_total = 0

def total(msg):
	# piggyback flag
	val = {'flag': 0, 'R': R_total, 'msg': msg}
	# basic multicast msg
	basic(val)

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
		flag = msg['flag']
		if flag == 0:
			seq, val = msg['R'], msg['msg']
			hbQueue.append((pid, seq, val))
		else:
			seq, pid = msg['S'], msg['pid']
			helper(seq, pid)

def totalSeqRecv(pid):
	if pid != str(ID):
		# construct msg
		msg = {'flag':1, 'S': S_total, 'pid':pid}
		# basic multicast msg
		basic(msg)
		# increment S_Total
		S_total += 1

def causalInit():
	# vector timestamp init
	global V_causal
	V_causal = [0 for idx in len(config_map.keys)]

def causal(msg):
	# increment V[i] by 1
	V_causal[ID] += 1
	# piggy back vector timestamp
	val = {'vec': V_causal, 'msg':msg}
	# basic mult
	basic(val)

def causalRecv(pid, msg):
	def helper(sender, vec, val):
		# place val in hold-back queue
		hbQueue.insert(0,(sender, vec, msg))
		# loop through queue
		for val in hbQueue:
			sender, vec, msg = val
			if vec[sender] == V_causal[sender] + 1:
				flag = True
				for idx in xrange(len(V_causal)):
					if vec[idx] > V_causal[idx]:
						flag = False
				if flag:
					deliever(sender, msg)
	vec, val = msg['vec'], msg['msg']
	helper(pid, vec, val)

def deliever(sender, msg):
	print sender, time.time(), msg

inits = [fifoInit, totalInit, causalInit]
orders = [fifo, total, causal]
recvs = [fifoRecv, totalRecv, causalRecv]

def Main():
	order, maxServer = sys.argv[2:4]
	# init node
	inits[int(order)]()
	global node
	print maxServer
	node = unicast.Unicast(config_map, int(maxServer), delay_range, config_inv, recvs[int(order)])
	
	while True:
		_,msg = raw_input().split(" ",1)
		orders[int(order)](msg)

if __name__ == "__main__":
	Main()