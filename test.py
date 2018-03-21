import unicast
import multicast
import sys
import time

def Main():
	pid, maxServer, order, numMsg = sys.argv[1:5]
	node = multicast.mults[order](pid, int(maxServer), unicast.delay_range)

	waitTime = int(maxServer)*int(numMsg) if order != 'total' else (int(maxServer)-1)*int(numMsg)

	time.sleep(5)

	system_time_start = time.time()
	for i in xrange(int(numMsg)*int(pid), int(numMsg)*(int(pid)+1) ):
		node.send(str(i))

	
	while node.num_deliver < waitTime:
		continue
	system_time_stop = time.time()
	node.send('bye')
	print "\nSend %s msg with %s ordering takes %f s\n" % (numMsg, order, system_time_stop - system_time_start)

if __name__ == "__main__":
	Main()