import requests
import threading
import socket
import time
from flask import Flask, request
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from zeroconf_browse import ServiceMonitor

server_ip = '192.168.1.110'
server_port = 1698

app = Flask(__name__)

@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    data = request.data.decode("utf-8")
    print("Received data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"

def run_flask_app():
    app.run(host= server_ip, port = server_port, debug=False)
    
# Start the Flask application in a new thread
threading.Thread(target=run_flask_app, daemon=True).start()
time.sleep(1)
condition = threading.Condition()
listener = ServiceMonitor("nobino-avms._itxpt_http._tcp.local.", condition)
zeroconf = Zeroconf()
print("Waiting for nobino-avms._itxpt_http._tcp.local. to be published...")
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
            time.sleep(60)
            runmonitoring_unsubscription(ip_address, port, path)
            
             
def runmonitoring_subscription(service_ip, service_port, path):
    subscription_request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request_xml)


    response = requests.post(f'http://{service_ip}:{service_port}/{path}runmonitoring', headers = {'Content-Type': 'application/xml'}, data=subscription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
def runmonitoring_unsubscription(service_ip, service_port, path, operations):
    unsubcription_request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <!-- ITxPT S02P00 Networks and Protocols - Unsubscribe request XML Example -->
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </UnsubscribeRequest>"""
    print(unsubcription_request_xml)
    
    response = requests.post(f'http://{service_ip}:{service_port}/{path}{operations}', headers = {'Content-Type': 'application/xml'}, data=unsubcription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
# Start the background thread
threading.Thread(target=print_info, args=(listener, condition), daemon=True).start()

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()




