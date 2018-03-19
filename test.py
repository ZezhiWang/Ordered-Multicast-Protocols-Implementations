import unicast
import multicast
import sys
import time

def Main():
	pid, maxServer, order, numMsg = sys.argv[1:5]
	node = multicast.mults[order](pid, int(maxServer), unicast.delay_range)

	time.sleep(5)

	system_time_start = time.time()
	for i in xrange(int(numMsg)*int(pid), int(numMsg)*(int(pid)+1) ):
		#time.sleep(0.1)
		node.send(str(i))

	while node.num_deliver < int(maxServer)*int(numMsg):
		continue
	system_time_stop = time.time()
	node.send('bye')
	print "\nSend %s msg with %s ordering takes %f s\n" % (numMsg, order, system_time_stop - system_time_start)

if __name__ == "__main__":
	Main()