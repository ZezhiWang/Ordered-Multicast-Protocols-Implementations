import socket
import sys
import traceback
from threading import Thread

config_map = {}
config_inv = {}
def parse_config(filename):
    config = open(filename, "r")
    for line in config:
        lineList = line.split()
        print lineList
        config_map[lineList[0]] = (lineList[1], int(lineList[2]))
        config_inv[(lineList[1], int(lineList[2])] = lineList[0]

def unicast_send(destination, message):
    #get the ip address and port number of config file
    host, port = config_map[destination]

    #connect to host/port
    sock.connect((host, port))

    #send the message
    sock.send(message)
