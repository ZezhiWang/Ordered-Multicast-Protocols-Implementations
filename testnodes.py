import os

for i in xrange(4,12,4):
	for j in xrange(i):
		os.system("python test.py %d %d fifo 3 &" % (j, i))
