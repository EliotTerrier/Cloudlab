import requests
import time
import _thread
import threading
import xml.etree.ElementTree as ET
from flask import Flask, Response, request
from service_discovery import publish_service
import Data
from subscription_functions import handle_subscription, daemon

#avms service parameters 
name = "ITxPT_avms"
ipaddress = "10.0.9.227"
port = 8000
service_type = "_itxpt_http._tcp.local."
properties = {
	'txtvers': '1',
	'version': '2.2.1',
	'path':'avms/',
	'operation':'runmonitoring;plannedpattern;vehiclemonitoring;journeymonitoring;'
}
app = Flask(__name__)

runmonitoring_ip_list = []
runmonitoring_port_list = []
runmonitoring_path_list = []

plannedpattern_ip_list = []
plannedpattern_port_list = []
plannedpattern_path_list = []

vehiclemonitoring_ip_list = []
vehiclemonitoring_port_list = []
vehiclemonitoring_path_list = []

journeymonitoring_ip_list = []
journeymonitoring_port_list = []
journeymonitoring_path_list = []

# import the XML templates
XMLRunMonitoringTemplate=Data.XMLRunMonitoringTemplate
XMLPlannedPatternTemplate=Data.XMLPlannedPatternTemplate
XMLVehicleMonitoringTemplate=Data.XMLVehicleMonitoringTemplate
XMLJourneyMonitoringTemplate=Data.XMLJourneyMonitoringTemplate



def publish_zeroconf_service():  
	threading.Thread(target=publish_service, daemon=True, args=(name, service_type, ipaddress, port, properties)).start() # daemon=True to exit the subscrption process when the flask server is stopped

@app.route('/avms/runmonitoring', methods=['POST'])
def runmonitoring_subscription():
	return handle_subscription(runmonitoring_ip_list, runmonitoring_port_list, runmonitoring_path_list)
	
 
@app.route('/avms/plannedpattern', methods=['POST'])
def plannedpattern_subscription():
	return handle_subscription(plannedpattern_ip_list, plannedpattern_port_list, plannedpattern_path_list)
    
@app.route('/avms/vehiclemonitoring', methods=['POST'])
def vehiclemonitoring_subscription():
	return handle_subscription(vehiclemonitoring_ip_list, vehiclemonitoring_port_list, vehiclemonitoring_path_list)
    
@app.route('/avms/journeymonitoring', methods=['POST'])
def journeymonitoring_subscription():
	return handle_subscription(journeymonitoring_ip_list, journeymonitoring_port_list, journeymonitoring_path_list)
    
def runmonitoring_daemon():
	return daemon(runmonitoring_ip_list, runmonitoring_port_list, runmonitoring_path_list, XMLRunMonitoringTemplate)

def plannedpattern_daemon():
	return daemon(plannedpattern_ip_list, plannedpattern_port_list, plannedpattern_path_list, XMLPlannedPatternTemplate)
  
def vehiclemonitoring_daemon():
	return daemon(vehiclemonitoring_ip_list, vehiclemonitoring_port_list, vehiclemonitoring_path_list, XMLVehicleMonitoringTemplate)

def journeymonitoring_daemon():
	return daemon(journeymonitoring_ip_list, journeymonitoring_port_list, journeymonitoring_path_list, XMLJourneyMonitoringTemplate)
  
def background_job():
    print("AVMS server started and waiting for client and/or delivery dispatch")
    while True:
        #print(("Total number of IPs in the list:", len(runmonitoring_ip_list)))
        rmd = threading.Thread(target=runmonitoring_daemon, name='Thread-rm')
        rmd.daemon = True
        
        ppd = threading.Thread(target=plannedpattern_daemon, name='Thread-pp')
        ppd.daemon = True
        
        vmd = threading.Thread(target=vehiclemonitoring_daemon, name='Thread-vm')
        vmd.daemon = True
        
        jmd = threading.Thread(target=journeymonitoring_daemon, name='Thread-jm')
        jmd.daemon = True
  
        rmd.start()
        ppd.start()
        vmd.start()
        jmd.start()
        time.sleep(5)


# thread will automatically exit when the main program finishes

if __name__ == '__main__':

    _thread.start_new_thread(background_job, ())
    publish_zeroconf_service()
    app.run(host=ipaddress, port=port, debug=False)
	

