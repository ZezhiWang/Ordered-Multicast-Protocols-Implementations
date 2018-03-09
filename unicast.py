import socket
import sys
import traceback
from threading import Thread


def unicast_receive(source, message):
	print "Process" + source + ": " + message

def socket_listen_thread(sock):
	sock.listen(5)
	print "Socket now listening..."

	while True:
		conn, address = sock.accept()

		ip, port = str(address[0]), str(address[1])
		message = conn.recv(1024)
		unicast_receive(config_inv(ip, port), message)
		conn.close()


def main(id):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((config_map[id][0], config_map[id][1]))

	Thread(target=socket_listen_thread, args=(sock)).start()

