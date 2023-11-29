import requests
import time
import _thread
import threading
import xml.etree.ElementTree as ET
from flask import Flask, Response, request
from zeroconf_publish import publish_service

#avms service parameters 
name = "nobino-avms"
ipaddress = "192.168.1.105"
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

XMLRunMonitoringTemplate='''<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Run Monitoring operation XML Example -->
<RunMonitoringDelivery version="2.2.1">
  <MonitoredRunState>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <MonitoredBlockRef>9301</MonitoredBlockRef>
    <CurrentRunInfo>
      <RunState>RunPattern</RunState>
      <PatternRunType>ServiceJourneyPattern</PatternRunType>
      <JourneyPatternRef>9308</JourneyPatternRef>
      <VehicleJourneyRef>930110</VehicleJourneyRef>
    </CurrentRunInfo>
    <RunningPatternState>OnDiversion</RunningPatternState>
    <NextRunInfo>
      <RunState>RunToPattern</RunState>
      <PatternRunType>ServiceJourneyPattern</PatternRunType>
      <JourneyPatternRef>9311</JourneyPatternRef>
      <VehicleJourneyRef>930111</VehicleJourneyRef>
    </NextRunInfo>
    <MonitoredRunStateNote>Note</MonitoredRunStateNote>
  </MonitoredRunState>
</RunMonitoringDelivery>'''


def publish_zeroconf_service():  
	threading.Thread(target=publish_service, daemon=True, args=(name, service_type, ipaddress, port, properties)).start() # daemon=True to exit the subscrption process when the flask server is stopped

@app.route('/avms/runmonitoring', methods=['POST'])
def runmonitoring_subscription():

	with open("last_avms_sub_req.xml", "w") as xml_file:
		unparsed=request.get_data().decode("utf-8")
		xml_file.write(unparsed)
	try:
		tree = ET.parse('last_avms_sub_req.xml')
		root = tree.getroot()
		if root.tag =="SubscribeRequest":
			
			IP_address = root.findall('Client-IP-Address')
			if len(IP_address)>0:
				for ip in root.iter('Client-IP-Address'):
						client_ip = ip.text
				port_number = root.findall('ReplyPort')
				if len(port_number)>0:
					for port in root.iter('ReplyPort'):
						reply_port = port.text
					path = root.findall('ReplyPath')
					if len(path)>0:
						for pth in root.iter('ReplyPath'):
							reply_path = pth.text
						subscribe_response = '''<?xml version="1.0" encoding="UTF-8"?><SubscribeResponse><Active>true</Active></SubscribeResponse>'''
						if client_ip in runmonitoring_ip_list:
							runmonitoring_port_list[runmonitoring_ip_list.index(client_ip)]=reply_port
							runmonitoring_path_list[runmonitoring_ip_list.index(client_ip)]=reply_path
						else:
							runmonitoring_ip_list.append(client_ip)
							runmonitoring_port_list.append(reply_port)
							runmonitoring_path_list.append(reply_path)
						resp = Response(subscribe_response, status=200, mimetype='application/xml')
						return resp
					else:
						return Response(status=422, body="Could not find Reply Path structure.")
				else:
					return Response(status=422, body="Could not find Reply Port structure.")
			else:
				return Response(status=422, body="Could not find Client-IP-Address field.")	
		elif root.tag =="UnsubscribeRequest":
			IP_address = root.findall('Client-IP-Address')
			if len(IP_address)>0:
				for ip in root.iter('Client-IP-Address'):
						client_ip = ip.text
				port_number = root.findall('ReplyPort')
				if len(port_number)>0:
					for port in root.iter('ReplyPort'):
						reply_port = port.text
					path = root.findall('ReplyPath')
					if len(path)>0:
						for pth in root.iter('ReplyPath'):
							reply_path = pth.text
						unsubscribe_response = '''<?xml version="1.0" encoding="UTF-8"?><UnsubscribeResponse><Active>false</Active></UnsubscribeResponse>'''
						if client_ip in runmonitoring_ip_list:
							ind = runmonitoring_ip_list.index(client_ip)
							del runmonitoring_ip_list[ind]
							del runmonitoring_port_list[ind]
							del runmonitoring_path_list[ind]
							resp = Response(unsubscribe_response, status=200, mimetype='application/xml')
							return resp
						else:
							return Response(status=422, body="Could not find client ("+client_ip+") in the list.")
					else:
						return Response(status=422, body="Could not find Reply Path structure.")
				else:
					return Response(status=422, body="Could not find Reply Port structure.")
			else:
				return Response(status=422, body="Could not find Client-IP-Address field.")
		else: 
			return Response(status=422, body="Could not find SubscribeRequest structure.")
	except:
		return Response(status=422, body="Could not validate XML SubscribeRequest integrity.")
	
    

def runmonitoring_daemon():

    for IP in runmonitoring_ip_list:
		
        port_to_use = runmonitoring_port_list[runmonitoring_ip_list.index(IP)]
        path_to_use = runmonitoring_path_list[runmonitoring_ip_list.index(IP)]
        res = requests.post('http://' + IP + ':' + port_to_use + path_to_use,headers={'Content-type': 'application/xml'},data=bytearray(XMLRunMonitoringTemplate,encoding="utf-8"))
        print("Run monitoring delivery to: " + str(IP) + " get status: " + str(res.status_code))


def background_job():
    print("AVMS server started and waiting for client and/or delivery dispatch")
    while True:
        #print(("Total number of IPs in the list:", len(runmonitoring_ip_list)))
        rmd = threading.Thread(target=runmonitoring_daemon, name='Thread-rm')
        rmd.daemon = True
        rmd.start()
        time.sleep(1)


# thread will automatically exit when the main program finishes

if __name__ == '__main__':

    _thread.start_new_thread(background_job, ())
    publish_zeroconf_service()
    app.run(host=ipaddress, port=port, debug=False)
	

