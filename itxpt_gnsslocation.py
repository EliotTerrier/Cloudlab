import socket, signal
import threading
import time
import Data
import xml.etree.ElementTree as ET
from datetime import datetime
from service_discovery import publish_service

MCAST_GRP = '239.255.42.21'
MULTICAST_TTL = 2


#gnsslocation service parameters 
name = "ITxPT_gnsslocation"
ipaddress = "10.0.9.227"
port = 14005
service_type = "_itxpt_multicast._udp.local."
properties = {
	'txtvers': '1',
	'version': '2.2.1',
    'multicast': MCAST_GRP
}

killService = False
xml_data= Data.GNSSLocationDeliveryTemplate


def publish_zeroconf_service():  
	threading.Thread(target=publish_service, daemon=True, args=(name, service_type, ipaddress, port, properties)).start() # daemon=True to exit the subscrption process when the flask server is stopped


def exit_gracefully(signum,frame):
    global killService
    killService = True

def changeXMLData(xml_data, longitude, latitude):
    xml = ET.fromstring(xml_data)  # Convert string to ElementTree object
    xml.find(".//Data").text = ""  # Empty data string 
    currentdate = datetime.today()
    xml.find(".//Latitude/Degree").text = "48.877583"
    xml.find(".//Longitude/Degree").text = f"{longitude:.6f}"  # Update longitude value 
    xml.find(".//Time").text = currentdate.strftime("%H:%M:%S")
    xml.find(".//Date").text = currentdate.strftime("%Y-%m-%d")
    return ET.tostring(xml, encoding="utf-8", xml_declaration=True)  # Convert the modified ElementTree object back to a string


def gnsslocation_daemon(ipaddress,port,xmlData):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    # limit multicast to a specific interface
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(ipaddress))
    sock.sendto(bytearray(xmlData), (MCAST_GRP, port))

def background_job():
        global killService
        global xml_data
        global port
        global ipaddress

        print("GNSSLocation server started and delivering UDP packets to multicast group")
        publish_zeroconf_service()
        longitude=2.338950
        while not killService:
                time.sleep(1)
                xmlData=changeXMLData(xml_data,longitude,0)
                longitude+=1E-6 #going east every second
                print(xmlData)
                gnss_thread = threading.Thread(target=gnsslocation_daemon, name='Thread-gnss_thread',kwargs={"ipaddress":ipaddress,"port":port,"xmlData":xmlData})
                gnss_thread.daemon = True
                gnss_thread.start()
        if  gnss_thread!=None and gnss_thread.is_alive():
            gnss_thread.join()
        print("Service terminated gracefully.")

     
# main 
if __name__ == '__main__':

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    background_job()
    
