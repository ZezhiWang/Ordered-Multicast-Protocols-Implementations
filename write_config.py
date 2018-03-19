def write_config(filename):
	with open(filename, "w") as config:
		for i in xrange(100):
			config.write("%d 127.0.0.1 %d\n" % (i, 8880+i))

if __name__ == "__main__":
	write_config("config.txt")