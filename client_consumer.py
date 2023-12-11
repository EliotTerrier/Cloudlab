import requests
import threading
import socket
import time
from flask import Flask, request
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from service_discovery import ServiceMonitor, publish_service
from subscription_functions import subscription_request, unsubscription_request


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
                service_ip = socket.inet_ntoa(address)
                print(f"Service address: {service_ip}")
            service_port=service_info.port
            # Create a new dictionary to hold the decoded properties
            properties = {k.decode('utf-8'): v.decode('utf-8') for k, v in service_info.properties.items()}
            path = properties.get('path')
            #operations = properties.get('operation')
            print(f"Service path: {path}")
            #print(f"Service operations: {operations}")
            subscription_request(service_ip, service_port, path, 'runmonitoring', server_ip, server_port, '/RunMonitoringDeliveryReply/1')
            subscription_request(service_ip, service_port, path, 'plannedpattern', server_ip, server_port, '/PlannedPatternDeliveryReply/1')
            subscription_request(service_ip, service_port, path, 'vehiclemonitoring', server_ip, server_port, '/VehicleMonitoringDeliveryReply/1')
            subscription_request(service_ip, service_port, path, 'journeymonitoring', server_ip, server_port, '/JourneyMonitoringDeliveryReply/1')
            time.sleep(30)
            unsubscription_request(service_ip, service_port, path, 'runmonitoring', server_ip, server_port, '/RunMonitoringDeliveryReply/1')
            unsubscription_request(service_ip, service_port, path, 'plannedpattern', server_ip, server_port, '/PlannedPatternDeliveryReply/1')
            unsubscription_request(service_ip, service_port, path, 'vehiclemonitoring', server_ip, server_port, '/VehicleMonitoringDeliveryReply/1')
            unsubscription_request(service_ip, service_port, path, 'journeymonitoring', server_ip, server_port, '/JourneyMonitoringDeliveryReply/1')        
          
# Start the background thread
threading.Thread(target=print_info, args=(listener, condition), daemon=True).start()

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()




