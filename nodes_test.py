import unicast
import multicast
import sys
import time
import multiprocessing


def Main():
	'''
		Test for scalability in number of message

		set number of message sent in each node:
		5
		10
		20
		40
		80
		160
	'''
	pid, maxServer, order, __= sys.argv[1:5]
	#create a multicast node 
	node = multicast.mults[order](pid, int(maxServer), unicast.delay_range)

	
	#hard-coding make sure every one is ready
	time.sleep(10)

	#to hold time for different number of message
	time_record = []

	#manually set values
	number_of_message = [1, 5, 10, 15, 20]

	#for each test cases
	for numMsg in number_of_message:

		#calculated waitTime for deliver
		waitTime = int(maxServer)*int(numMsg) if order != 'total' else (int(maxServer)+1)*int(numMsg)

		#start record time
		system_time_start = time.time()
		#send msg with 1 sec delay each time (avoid Too many socket openning)
		for i in xrange(int(numMsg)*int(pid), int(numMsg)*(int(pid)+1) ):
			time.sleep(1)
			node.send(str(i))

		#wait for all the msg delivered
		while node.num_deliver < waitTime:
			continue
		#record the ending time
		system_time_stop = time.time()
		#append to time record
		time_record.append(system_time_stop - system_time_start)

	#send bye to end
	node.send('bye')
	print time_record



if __name__ == "__main__":
	Main()
	