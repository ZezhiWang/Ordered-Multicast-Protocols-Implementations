import unicast
import multicast

def Main():
	pid, maxServer, order, numMsg = sys.argv[1:5]
	node = multicast.mults[order](pid, int(maxServer), unicast.delay_range)

	system_time_start = time.time()
	for i in xrange(int(numMsg)):
		node.send(str(i))
	while node.num_deliver < int(numMsg):
		continue
	system_time_stop = time.time()
	node.send('bye')
	print "Send %s msg with %s ordering takes %f ms", % (numMsg, order, system_time_stop - system_time_start)

if __name__ == "__main__":
	Main()