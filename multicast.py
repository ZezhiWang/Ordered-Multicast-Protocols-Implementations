import unicast
import time
import sys
from threading import Thread

config_map = unicast.config_map

class FifoMult:
	def __basic(self, msg):
		for idx in config_map.keys():
			self.node.unicast_send(idx, msg)

	def __deliever(self, sender, msg):
		print sender, time.time(), msg

	def send(self, msg):
		# increment S by 1
		self.S_fifo += 1
		# piggy back S into msg
		val = {'seq':self.S_fifo, 'msg':msg}
		# B-multicast
		self.__basic(val)

	def recv(self,pid, msg):
		def helper(sender, seq, msg):
			# if S = R[q] + 1
			if seq == self.R_fifo[sender] + 1:
				# Fifo deliever msg
				self.__deliever(sender, msg)
				# increment R[q]
				self.R_fifo[sender] += 1
			# if S > R[q]
			elif seq > self.R_fifo[sender] + 1:
				# put msg in hold-back queue
				self.hbQueue.append((sender,seq,msg))
			# check msg in hold-back queue
			for val in self.hbQueue:
				sender,seq,msg = val
				if seq == self.R_fifo[sender] + 1:
					self.hbQueue.remove(val)
					self.__deliever(sender, msg)
					self.R_fifo[sender] += 1
			# else reject
			return
		seq, val = msg['seq'], msg['msg']
		helper(int(pid), seq, val)

	def __init__(self, pid, maxServer, delay_range):
		# num of msg cur server has sent to group
		self.S_fifo = 0
		# seq num of latest group msg cur server has delievered from other server
		self.R_fifo = [0 for i in config_map.keys()]
		# init unicast client
		self.node = unicast.Unicast(pid, maxServer, delay_range, self.recv)
		# hold-back queue
		self.hbQueue = []

class TotalMult:
	def __basic(self, msg):
		for idx in config_map.keys():
			self.node.unicast_send(idx, msg)

	def __deliever(self, sender, msg):
		print sender, time.time(), msg

	def send(self, msg):
		# piggyback flag
		val = {'flag': 0, 'R': self.R_total, 'msg': msg}
		# basic multicast msg
		self.__basic(val)

	def __seqRecv(self, pid):
		if pid != self.pid:
			# construct msg
			msg = {'flag':1, 'S': self.S_total, 'pid':pid}
			# basic multicast msg
			self.__basic(msg)
			# increment S_Total
			self.S_total += 1

	def recv(self, pid, msg):
		def helper(seq, pid):
			for val in self.hbQueue:
				sender, seqTmp, msg = val
				if seqTmp == seq:
					self.hbQueue.remove(val)
					self.__deliever(sender, msg)
					self.R_total += 1
		if pid == '0':
			self.__seqRecv(pid)
		else:
			# split senderID and seq and msg from val
			flag = msg['flag']
			if flag == 0:
				seq, val = msg['R'], msg['msg']
				self.hbQueue.append((pid, seq, val))
			else:
				seq, pid = msg['S'], msg['pid']
				helper(seq, pid)

	def __init__(self, pid, maxServer, delay_range):
		# hold-back queue
		self.hbQueue = []
		if int(pid) == 0:
			# init sequencer
			self.S_total = 0
		else:
			# init group member
			self.R_total = 0
		# init unicast client
		self.node = unicast.Unicast(pid, int(maxServer), delay_range, self.recv)


class CausalMult:
	def __basic(self, msg):
		for idx in config_map.keys():
			self.node.unicast_send(idx, msg)

	def __deliever(self, sender, msg):
		print sender, time.time(), msg

	def send(self,msg):
		# increment V[i] by 1
		self.V_causal[self.pid] += 1
		# piggy back vector timestamp
		val = {'vec': self.V_causal, 'msg':msg}
		# basic mult
		self.__basic(val)
	
	def recv(self, pid, msg):
		def helper(sender, vec, val):
			# place val in hold-back queue
			self.hbQueue.append((sender, vec, val))
			# loop through queue
			for val in self.hbQueue:
				sender, vec, msg = val
				if vec[sender] == self.V_causal[sender] + 1:
					flag = True
					for idx in xrange(len(config_map.keys())):
						if vec[idx] > self.V_causal[idx]:
							flag = False
					if flag:
						self.__deliever(sender, val)
		vec, val = msg['vec'], msg['msg']
		helper(int(pid), vec, val)

	def __init__(self, pid, maxServer, delay_range):
		# hold-back queue
		self.hbQueue = []
		self.pid = int(pid)
		# vector timestamp init
		self.V_causal = [0 for idx in config_map.keys()]
		# init unicast client
		self.node = unicast.Unicast(pid, maxServer, delay_range, self.recv)


mults = [FifoMult, TotalMult, CausalMult]


def Main():
	pid, order, maxServer = sys.argv[1:4]
	# delayRange
	delay_range = 5
	
	node = mults[int(order)](pid, int(maxServer), delay_range)
	
	while True:
		_,msg = raw_input().split(" ",1)
		node.send(msg)

if __name__ == "__main__":
	Main()