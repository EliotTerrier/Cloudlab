import socket
import struct
import threading
import time
from zeroconf import Zeroconf, ServiceBrowser
from service_discovery import ServiceMonitor

MCAST_GRP = None # multicast group
MCAST_PORT = None # multicast port

condition = threading.Condition()
listener = ServiceMonitor("gnsslocation", condition)
zeroconf = Zeroconf()
print("Waiting for gnsslocation service...")
browser = ServiceBrowser(zeroconf, "_itxpt_multicast._udp.local.", listener)

def print_info(listener, condition):
    global MCAST_GRP, MCAST_PORT
    while True:
        with condition:
            condition.wait()
        info = listener.getInfo()
        for name, service_info in info.items():
            print(f"Service name: {name}")
            MCAST_PORT = service_info.port
            properties = {k.decode('utf-8'): v.decode('utf-8') for k, v in service_info.properties.items()}
            MCAST_GRP = properties.get('multicast')

info_thread = threading.Thread(target=print_info, daemon= True, args=(listener, condition))
info_thread.start()

while MCAST_GRP is None or MCAST_PORT is None:
    time.sleep(1)  # wait for MCAST_GRP and MCAST_PORT to be set

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # create a new UDP socket.
sock.bind((MCAST_GRP, MCAST_PORT)) # bind the socket to the multicast group and port.

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY) # creates a binary data structure that's used to tell the operating system to add the socket to the multicast group.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) # add the socket to the multicast group.

while True:
    print(sock.recv(10240)) # wait for data to be received from the multicast group and then prints it (10240 = maximum amount of data that will be received at once.)
