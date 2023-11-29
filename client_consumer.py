import requests
import threading
import socket
from flask import Flask, request
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
from zeroconf_browse import ServiceMonitor



app = Flask(__name__)

@app.route('/RunMonitoringDeliveryReply/1', methods=['POST'])   
def runmonitoring_reply():
    data = request.data.decode("utf-8")
    print("Received data:", data)
    # Add your logic to process the received data here
    return "Data received successfully"

def run_flask_app():
    app.run(host='192.168.1.110', port=1698, debug=False)
    
# Start the Flask application in a new thread
threading.Thread(target=run_flask_app, daemon=True).start()

condition = threading.Condition()
listener = ServiceMonitor("nobino-avms._itxpt_http._tcp.local.", condition)
zeroconf = Zeroconf()
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
            print(f"Service port: {port}")
            runmonitoring_subscription(ip_address, port)

def runmonitoring_subscription(service_ip, service_port):
    subscription_request_xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>192.168.1.110</Client-IP-Address>
        <ReplyPort>1698</ReplyPort>
        <ReplyPath>/RunMonitoringDeliveryReply/1</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request_xml)


    response = requests.post(f'http://{service_ip}:{service_port}/avms/runmonitoring', headers = {'Content-Type': 'application/xml'}, data=subscription_request_xml)
    response.raise_for_status()  # Raises HTTPError for bad responses

# Start the background thread
threading.Thread(target=print_info, args=(listener, condition), daemon=True).start()

try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()




