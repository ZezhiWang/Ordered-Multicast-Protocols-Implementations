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
		print "    Receive %s from process %d with time %f" % ( msg, sender, time.time())
		return msg == 'bye'

	def isUp(self):
		return self.node.isRunning()

	def send(self, msg):
		# increment S by 1
		self.S_fifo += 1
		# piggy back S into msg
		val = {'seq':self.S_fifo, 'msg':msg}
		# basic multicast msg
		self.__basic(val)

	def recv(self, pid, msg):
		def helper(sender, seq, msg):
			res = False
			# if S = R[q] + 1
			if seq == self.R_fifo[sender] + 1:
				# Fifo deliever msg
				res = self.__deliever(sender, msg)
				# increment R[q]
				self.R_fifo[sender] += 1
			# if S > R[q]
			elif seq > self.R_fifo[sender] + 1:
				# put msg in hold-back queue
				self.hbQueue.append((sender,seq,msg))
			# check msg in hold-back queue
			for i in xrange(len(self.hbQueue)):				
				for val in self.hbQueue:
					sender,seq,msg = val
					if seq == self.R_fifo[sender] + 1:
						self.hbQueue.remove(val)
						res = self.__deliever(sender, msg)
						self.R_fifo[sender] += 1
			# else reject
			return res
		seq, val = msg['seq'], msg['msg']
		return helper(int(pid), seq, val)

	def __init__(self, pid, maxServer, delay_range):
		# self pid
		self.pid = pid
		# num of msg cur server has sent to group
		self.S_fifo = 0
		# seq num of latest group msg cur server has delievered from other server
		self.R_fifo = [0 for i in config_map.keys()]
		self.maxServer = maxServer
		# init unicast client
		self.node = unicast.Unicast(pid, maxServer, delay_range, self.recv)
		# hold-back queue
		self.hbQueue = []

class TotalMult:
	def __basic(self, msg):
		for idx in config_map.keys():
			self.node.unicast_send(idx, msg)

	def __deliever(self, sender, msg):
		print "Receive %s from process %s with time %f" % ( msg, sender, time.time())
		return msg == 'bye'

	def isUp(self):
		return self.node.isRunning()

	def send(self, msg):
		# piggyback flag
		val = {'flag': 0, 'I': self.S_total, 'msg': msg}
		# increment R_total
		self.S_total += 1
		# basic multicast msg
		self.__basic(val)

	def __seqRecv(self, pid, data):
		print "Sequencer received msg from", pid
		if pid != self.pid:
			# construct msg
			msg = {'flag':1, 'S': self.S_total, 'pid':pid, 'msg': "fk", 'I':data['I']}
			# basic multicast msg
			self.__basic(msg)
			# increment S_Total
			self.S_total += 1

	def recv(self, pid, msg):
		def helper():
			# wait until S = r in hbQueue
			for data in self.seqs:
				seq, pid, I = data
				for val in self.hbQueue:
					sender, idx, msg = val
					if idx == I and sender == pid and seq == self.R_total:
						self.hbQueue.remove(val)
						self.seqs.remove(data)
						if self.__deliever(sender, msg):
							return True
						self.R_total = seq + 1
			return False
		if self.pid == '0':
			self.__seqRecv(pid, msg)
		else:
			# split senderID and seq and msg from val
			flag = msg['flag']
			# if not from sequencer
			if flag == 0:
				idx, val = msg['I'], msg['msg']
				# add msg to hold-back queue
				self.hbQueue.append((pid, idx, val))
			else:
				seq, pid, I = msg['S'], msg['pid'], msg['I']
				self.seqs.append((seq, pid, I))
			helper()
		return False

	def __init__(self, pid, maxServer, delay_range):
		# self pid
		self.pid = pid
		# hold-back queue
		self.hbQueue = []
		# hold-back queue for sequencer
		self.seqs = []
		self.S_total = 0
		if int(pid) != 0:
			# init group member
			self.R_total = 0
		# init unicast client
		self.maxServer = maxServer
		self.node = unicast.Unicast(pid, int(maxServer), delay_range, self.recv)

class CausalMult:
	def __basic(self, msg):
		for idx in config_map.keys():
			self.node.unicast_send(idx, msg)

	def __deliever(self, sender, msg):
		print "Receive %s from process %d with time %f" % ( msg, sender, time.time())
		return msg == 'bye'

	def isUp(self):
		return self.node.isRunning()

	def send(self,msg):
		# increment V[i] by 1
		self.V_causal[int(self.pid)] += 1
		# piggy back vector timestamp
		val = {'vec': self.V_causal, 'msg':msg}
		# basic multicast msg
		self.__basic(val)
	
	def recv(self, pid, msg):
		print "received a packet"
		def helper(sender, vec, val):
			# place val in hold-back queue
			self.hbQueue.append((sender, vec, val))
			# loop through queue
			#print "received ", vec
			#print "Us: ", self.V_causal
			res = False
			#print vec
			#print self.V_causal
			for i in range(len(self.hbQueue)):
				for val in self.hbQueue:
					sender, vec, msg = val
					if vec[sender] == self.V_causal[sender] + 1 or sender == int(self.pid): #make sure deliver myself
						flag = True
						for idx in xrange(len(config_map.keys())):
							if idx == int(self.pid) or idx == sender: 
								continue
							if vec[idx] > self.V_causal[idx]:
								flag = False
						#print flag
						if flag:
							res = self.__deliever(sender, msg)
							self.hbQueue.remove(val)
							if sender != int(self.pid):
								self.V_causal[sender] +=1
							#for idx in xrange(len(config_map.keys())):
								#if idx != int(self.pid):
									#self.V_causal[idx] = max(self.V_causal[idx], vec[idx])
			return res
			#print"after: ", self.V_causal
		vec, val = msg['vec'], msg['msg']
		return helper(int(pid), vec, val)

	def __init__(self, pid, maxServer, delay_range):
		# hold-back queue
		self.hbQueue = []
		# seld id
		self.pid = pid
		# vector timestamp init
		self.V_causal = [0 for idx in config_map.keys()]
		self.maxServer = maxServer
		# init unicast client
		self.node = unicast.Unicast(pid, maxServer, delay_range, self.recv)

mults = [FifoMult, TotalMult, CausalMult]

def Main():
	pid, order, maxServer = sys.argv[1:4]
	# delayRange
	delay_range = unicast.delay_range

	print "<<<<<<< chat room >>>>>>>>"
	
	node = mults[int(order)](pid, int(maxServer), delay_range)	
	while True:
		userInput = raw_input()
		if not node.isUp():
			break
		_,msg = userInput.split(" ",1)
		node.send(msg)

if __name__ == "__main__":
	Main()