import threading
import xml.etree.ElementTree as ET
from flask import Flask
from service_discovery import publish_service

app = Flask(__name__)
#service elements
name = "itxpt_inventory"
port = 9
service_type = "_itxpt_socket._tcp.local."
ipaddress = "10.0.9.227"
# Create TXT records as a dictionary
properties = {
    "txtvers": "1",
    "version": "2.1.1",
    "model": "model26",
    "manufacturer": "ITxPT",
    "serialnumber": "SN0123456789",
    "softwareversion": "v1.2.3",
    "hardwareversion": "revision D",
    "macaddress": "CF:DA:98:63:9D:F6",
    "status": "0",
    "services": "inventory;avms",
}

def publish_zeroconf_service():  
	threading.Thread(target=publish_service, daemon=True, args=(name, service_type, ipaddress, port, properties)).start() # daemon=True to exit the subscrption process when the flask server is stopped
 

if __name__ == '__main__':

    publish_zeroconf_service()
    app.run(host=ipaddress, port=port, debug=False)
