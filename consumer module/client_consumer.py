import requests
import threading
import socket
import time
from flask import Flask, request
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from service_discovery import ServiceMonitor, publish_service


server_ip = '10.0.9.208'
server_port = 1698
app = Flask(__name__)

name = "ITxPTconsumer_inventory"
port = 9
service_type = "_itxpt_socket._tcp.local."
ipaddress = server_ip
# Create TXT records as a dictionary
properties = {
    "txtvers": "1",
    "version": "2.2.1",
    "model": "model1",
    "manufacturer": "ITxPT",
    "serialnumber": "DS406420640210",
    "softwareversion": "v1.1.1",
    "hardwareversion": "revision J",
    "macaddress": "8a:74:08:b0:be:b7",
    "status": "0",
    "services": "inventory",
}

def publish_zeroconf_service():  
	threading.Thread(target=publish_service, daemon=True, args=(name, service_type, ipaddress, port, properties)).start() # daemon=True to exit the subscrption process when the flask server is stopped


@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    data = request.get_data().decode('utf-8')
    print("RunMonitoring data:", data)

    # Add your logic to process the received data here
    return "Data received successfully"

@app.route('/PlannedPatternDeliveryReply/1', methods=['POST'])   
def plannedpattern_reply():
    data = request.get_data().decode('utf-8')
    print("PlannedPattern data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"

@app.route('/VehicleMonitoringDeliveryReply/1', methods=['POST'])   
def vehiclemonitoring_reply():
    data = request.get_data().decode('utf-8')
    print("VehicleMonitoring data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"

@app.route('/JourneyMonitoringDeliveryReply/1', methods=['POST'])   
def journeymonitoring_reply():
    data = request.get_data().decode('utf-8')
    print("PlannedPattern data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"

def run_flask_app():
    app.run(host= server_ip, port = server_port, debug=False)
    
# Start the Flask application in a new thread
threading.Thread(target=run_flask_app, daemon=True).start()
publish_zeroconf_service()
time.sleep(1)
condition = threading.Condition()
listener = ServiceMonitor("avms", condition)
zeroconf = Zeroconf()
print("Waiting for avms service...")
browser = ServiceBrowser(zeroconf, "_itxpt_http._tcp.local.", listener)

def print_info(listener, condition):
    while True:
        with condition:
            condition.wait()
        info = listener.getInfo()
        for name, service_info in info.items():
            print(f"Service name: {name}")
            for address in service_info.addresses:
                ip_address = socket.inet_ntoa(address)
                print(f"Service address: {ip_address}")
            port=service_info.port
            # Create a new dictionary to hold the decoded properties
            properties = {k.decode('utf-8'): v.decode('utf-8') for k, v in service_info.properties.items()}
            path = properties.get('path')
            #operations = properties.get('operation')
            print(f"Service path: {path}")
            #print(f"Service operations: {operations}")
            runmonitoring_subscription(ip_address, port, path)
            plannedpattern_subscription(ip_address, port, path)
            vehiclemonitoring_subscription(ip_address, port, path)
            journeymonitoring_subscription(ip_address, port, path)
            time.sleep(30)
            runmonitoring_unsubscription(ip_address, port, path)
            plannedpattern_unsubscription(ip_address, port, path)
            vehiclemonitoring_unsubscription(ip_address, port, path)
            journeymonitoring_unsubscription(ip_address, port, path)
            
def runmonitoring_subscription(service_ip, service_port, path):
    runmonitoring_subcription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(runmonitoring_subcription_request)


    response = requests.post(f'http://{service_ip}:{service_port}/{path}runmonitoring', headers = {'Content-Type': 'application/xml'}, data=runmonitoring_subcription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
def runmonitoring_unsubscription(service_ip, service_port, path):
    runmonitoring_unsubcription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <!-- ITxPT S02P00 Networks and Protocols - Unsubscribe request XML Example -->
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </UnsubscribeRequest>"""
    print(runmonitoring_unsubcription_request)
    
    response = requests.post(f'http://{service_ip}:{service_port}/{path}runmonitoring', headers = {'Content-Type': 'application/xml'}, data=runmonitoring_unsubcription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
def plannedpattern_subscription(service_ip, service_port, path):
    plannedpattern_subscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/PlannedPatternDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(plannedpattern_subscription_request)


    response = requests.post(f'http://{service_ip}:{service_port}/{path}plannedpattern', headers = {'Content-Type': 'application/xml'}, data=plannedpattern_subscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses  

def plannedpattern_unsubscription(service_ip, service_port, path):
    plannedpattern_unsubscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/PlannedPatternDeliveryReply/1</ReplyPath>
    </UnsubscribeRequest>"""
    print(plannedpattern_unsubscription_request)


    response = requests.post(f'http://{service_ip}:{service_port}/{path}plannedpattern', headers = {'Content-Type': 'application/xml'}, data=plannedpattern_unsubscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses  

def vehiclemonitoring_subscription(service_ip, service_port, path):
    vehiclemonitoring_subscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/VehicleMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(vehiclemonitoring_subscription_request)


    response = requests.post(f'http://{service_ip}:{service_port}/{path}vehiclemonitoring', headers = {'Content-Type': 'application/xml'}, data=vehiclemonitoring_subscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses  

def vehiclemonitoring_unsubscription(service_ip, service_port, path):
    vehiclemonitoring_unsubscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/VehicleMonitoringDeliveryReply/1</ReplyPath>
    </UnsubscribeRequest>"""
    print(vehiclemonitoring_unsubscription_request)
    
    response = requests.post(f'http://{service_ip}:{service_port}/{path}vehiclemonitoring', headers = {'Content-Type': 'application/xml'}, data=vehiclemonitoring_unsubscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses 
    
def journeymonitoring_subscription(service_ip, service_port, path):
    journeymonitoring_subscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/JourneyMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(journeymonitoring_subscription_request)
    
    response = requests.post(f'http://{service_ip}:{service_port}/{path}journeymonitoring', headers = {'Content-Type': 'application/xml'}, data=journeymonitoring_subscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses 

def journeymonitoring_unsubscription(service_ip, service_port, path):
    journeymonitoring_unsubscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/JourneyMonitoringDeliveryReply/1</ReplyPath>
    </UnsubscribeRequest>"""
    print(journeymonitoring_unsubscription_request)
    
    response = requests.post(f'http://{service_ip}:{service_port}/{path}journeymonitoring', headers = {'Content-Type': 'application/xml'}, data=journeymonitoring_unsubscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses 
          
# Start the background thread
threading.Thread(target=print_info, args=(listener, condition), daemon=True).start()

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()




