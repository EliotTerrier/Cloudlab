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

plannedpattern_ip_list = []
plannedpattern_port_list = []
plannedpattern_path_list = []

vehiclemonitoring_ip_list = []
vehiclemonitoring_port_list = []
vehiclemonitoring_path_list = []

journeymonitoring_ip_list = []
journeymonitoring_port_list = []
journeymonitoring_path_list = []

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

XMLPlannedPatternTemplate= """<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Planned Pattern operation XML Example -->
<PlannedPatternDelivery version="2.2.1">
  <PlannedPattern>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <PatternRef>9308</PatternRef>
    <VehicleJourneyRef>1234</VehicleJourneyRef>
    <OperatingDayDate>2012-12-13</OperatingDayDate>
    <RouteRef>10</RouteRef>
    <LineRef>93</LineRef>
    <PublishedLineLabel>Teor 3</PublishedLineLabel>
    <PublishedTtsLineLabel>Teor 3</PublishedTtsLineLabel>
    <DirectionRef>123</DirectionRef>
    <ExternalLineRef>T3</ExternalLineRef>
    <OriginName>Bizet</OriginName>
    <OriginShortName>Bizet</OriginShortName>
    <OriginLongName>Bizet</OriginLongName>
    <OriginTtsName>BIZÃ©T</OriginTtsName>
    <Via>
      <PlaceRef>11525</PlaceRef>
      <PlaceName language="fre">Eglise St-Jean</PlaceName>
      <PlaceName language="eng">St-Jean church</PlaceName>
    </Via>
    <DestinationPlaceRef>12180</DestinationPlaceRef>
    <DestinationName>Durecu-Lavoisier</DestinationName>
    <DestinationShortName>Durecu-Lavoisier</DestinationShortName>
    <DestinationLongName>Durecu-Lavoisier</DestinationLongName>
    <DestinationTtsName>DURÃ©CU-LAVOISIER</DestinationTtsName>
    <PatternStops>
      <PatternStop>
        <StopPointRef>10164</StopPointRef>
        <Order>1</Order>
        <StopPointName>Bizet</StopPointName>
        <StopPointShortName>Bizet</StopPointShortName>
        <StopPointLongName>Bizet</StopPointLongName>
        <StopPointTtsName>BIZÃ©T</StopPointTtsName>
      </PatternStop>
      <PatternStop>
        <StopPointRef>11524</StopPointRef>
        <Order>2</Order>
        <StopPointName language="fre">Eglise St-Jean</StopPointName>
        <StopPointName language="eng">St-Jean church</StopPointName>
        <StopPointShortName>Eglise St-Jean</StopPointShortName>
        <StopPointLongName>Eglise St-Jean</StopPointLongName>
        <StopPointTtsName>EGLISE SAINT-JEAN</StopPointTtsName>
      </PatternStop>
<!-- […] -->
      <PatternStop>
        <StopPointRef>12180</StopPointRef>
        <Order>2</Order>
        <StopPointName>Durecu-Lavoisier</StopPointName>
        <StopPointShortName>Durecu-Lavoisier</StopPointShortName>
        <StopPointLongName>Durecu-Lavoisier</StopPointLongName>
        <StopPointTtsName>DURÃ©CU-LAVOISIER</StopPointTtsName>
      </PatternStop>
    </PatternStops>
    <PlannedPatternNote>Note</PlannedPatternNote>
  </PlannedPattern>
</PlannedPatternDelivery>
"""

XMLVehicleMonitoringTemplate= """<?xml version="1.0" encoding="utf-8"?>
<!-- ITxPT S02P06 AVMS service - Vehicle Monitoring operation XML Example -->
<VehicleMonitoringDelivery version="2.2.1">
  <VehicleActivity>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>9</ItemIdentifier>
    <JourneyPatternRef>9311</JourneyPatternRef>
    <VehicleJourneyRef>1234</VehicleJourneyRef>
    <ProgressBetweenStops>
      <PreviousCallRef>
        <StopPointRef>12159</StopPointRef>
        <Order>7</Order>
      </PreviousCallRef>
      <MonitoredCallRef>
        <StopPointRef>11759</StopPointRef>
        <Order>8</Order>
        <VehicleAtStop>true</VehicleAtStop>
      </MonitoredCallRef>
      <LinkDistance>123.45</LinkDistance>
      <Percentage>98.12</Percentage>
    </ProgressBetweenStops>
    <VehicleActivityNote>Note</VehicleActivityNote>
  </VehicleActivity>
  <VehicleActivityCancellation>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>9310</ItemIdentifier>
    <PatternRef>123</PatternRef>
    <Reason>Reason</Reason>
  </VehicleActivityCancellation> 
</VehicleMonitoringDelivery>
"""
XMLJourneyMonitoringTemplate = """<JourneyMonitoringDelivery version="2.2.1">
  <!-- ITxPT S02P06 AVMS service - Journey Monitoring operation XML Example -->
  <MonitoredJourney>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>2</ItemIdentifier>
    <PatternRef>9311</PatternRef>
    <JourneyRef>9</JourneyRef>
    <VehicleJourneyRef>9310</VehicleJourneyRef>
    <JourneyNote>Note</JourneyNote>
    <HeadwayService>true</HeadwayService>
    <OriginPlannedDepartureTime>2019-10-24T12:10:00</OriginPlannedDepartureTime>
    <DestinationPlannedArrivalTime>2019-10-24T12:20:12</DestinationPlannedArrivalTime>
    <InCongestion>true</InCongestion>
    <InPanic>true</InPanic>
    <ProgressRate>slowProgress</ProgressRate>
    <Occupancy>full</Occupancy>
    <Delay>340</Delay>
    <ProgressStatus>str1234</ProgressStatus>
    <ProductCategoryRef>str1234</ProductCategoryRef>
    <ServiceFeatureRef>str1234</ServiceFeatureRef>
    <VehicleFeatureRef>str1234</VehicleFeatureRef>
    <PreviousCalls>
      <PreviousCall>
        <StopPointRef>12180</StopPointRef>
        <Order>1</Order>
        <ActualArrivalTime>2019-10-24T12:10:12</ActualArrivalTime>
        <ActualDepartureTime>2019-10-24T12:12:12</ActualDepartureTime>
      </PreviousCall>
    </PreviousCalls>
    <MonitoredCall>
      <StopPointRef>12157</StopPointRef>
      <Order>9</Order>
      <VehicleAtStop>false</VehicleAtStop>
      <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
      <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
      <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
      <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
    </MonitoredCall>
    <OnwardCalls>
      <OnwardCall>
        <StopPointRef>12157</StopPointRef>
        <Order>10</Order>
        <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
        <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
        <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
        <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
      </OnwardCall>
      <!-- […] -->
      <OnwardCall>
        <StopPointRef>10164</StopPointRef>
        <Order>31</Order>
        <PlannedArrivalTime>2019-10-24T12:25:00</PlannedArrivalTime>
        <ExpectedArrivalTime>2019-10-24T12:30:00</ExpectedArrivalTime>
        <PlannedDepartureTime>2019-10-24T12:51:12</PlannedDepartureTime>
        <ExpectedDepartureTime>2019-10-24T12:12:12</ExpectedDepartureTime>
      </OnwardCall>
    </OnwardCalls>
  </MonitoredJourney>
  <MonitoredJourneyCancellation>
    <RecordedAtTime>2019-10-24T12:12:12</RecordedAtTime>
    <ItemIdentifier>1</ItemIdentifier>
    <PatternRef>9309</PatternRef>
    <JourneyRef>9</JourneyRef> 
    <Reason>Reason</Reason>
  </MonitoredJourneyCancellation>
</JourneyMonitoringDelivery>"""

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
	
 
@app.route('/avms/plannedpattern', methods=['POST'])
def plannedpattern_subscription():

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
						if client_ip in plannedpattern_ip_list:
							plannedpattern_port_list[plannedpattern_ip_list.index(client_ip)]=reply_port
							plannedpattern_path_list[plannedpattern_ip_list.index(client_ip)]=reply_path
						else:
							plannedpattern_ip_list.append(client_ip)
							plannedpattern_port_list.append(reply_port)
							plannedpattern_path_list.append(reply_path)
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
						if client_ip in plannedpattern_ip_list:
							ind = plannedpattern_ip_list.index(client_ip)
							del plannedpattern_ip_list[ind]
							del plannedpattern_port_list[ind]
							del plannedpattern_path_list[ind]
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
    
@app.route('/avms/vehiclemonitoring', methods=['POST'])
def vehiclemonitoring_subscription():

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
						if client_ip in vehiclemonitoring_ip_list:
							vehiclemonitoring_port_list[vehiclemonitoring_ip_list.index(client_ip)]=reply_port
							vehiclemonitoring_path_list[vehiclemonitoring_ip_list.index(client_ip)]=reply_path
						else:
							vehiclemonitoring_ip_list.append(client_ip)
							vehiclemonitoring_port_list.append(reply_port)
							vehiclemonitoring_path_list.append(reply_path)
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
						if client_ip in vehiclemonitoring_ip_list: 
							ind = vehiclemonitoring_ip_list.index(client_ip)
							del vehiclemonitoring_ip_list[ind]
							del vehiclemonitoring_port_list[ind]
							del vehiclemonitoring_path_list[ind]
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
    
@app.route('/avms/journeymonitoring', methods=['POST'])
def journeymonitoring_subscription():

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
						if client_ip in journeymonitoring_ip_list:
							journeymonitoring_port_list[journeymonitoring_ip_list.index(client_ip)]=reply_port
							journeymonitoring_path_list[journeymonitoring_ip_list.index(client_ip)]=reply_path
						else:
							journeymonitoring_ip_list.append(client_ip)
							journeymonitoring_port_list.append(reply_port)
							journeymonitoring_path_list.append(reply_path)
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
						if client_ip in journeymonitoring_ip_list:
							ind = journeymonitoring_ip_list.index(client_ip)
							del journeymonitoring_ip_list[ind]
							del journeymonitoring_port_list[ind]
							del journeymonitoring_path_list[ind]
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

def plannedpattern_daemon():
	for IP in plannedpattern_ip_list:
		port_to_use = plannedpattern_port_list[plannedpattern_ip_list.index(IP)]
		path_to_use = plannedpattern_path_list[plannedpattern_ip_list.index(IP)]
		res = requests.post('http://'+IP+':'+port_to_use+path_to_use, headers = {'Content-type': 'application/xml'}, data=bytearray(XMLPlannedPatternTemplate,encoding="utf-8"))
		print("Planned pattern delivery to: " + str(IP) + " get status: " + str(res.status_code))
  
def vehiclemonitoring_daemon():
	for IP in vehiclemonitoring_ip_list:
		port_to_use = vehiclemonitoring_port_list[vehiclemonitoring_ip_list.index(IP)]
		path_to_use = vehiclemonitoring_path_list[vehiclemonitoring_ip_list.index(IP)]
		res = requests.post('http://'+IP+':'+port_to_use+path_to_use, headers = {'Content-type': 'application/xml'}, data=bytearray(XMLVehicleMonitoringTemplate,encoding="utf-8"))
		print("Vehicle monitoring delivery to: " + str(IP) + " get status: " + str(res.status_code))

def journeymonitoring_daemon():
	for IP in journeymonitoring_ip_list:
		port_to_use = journeymonitoring_port_list[journeymonitoring_ip_list.index(IP)]
		path_to_use = journeymonitoring_path_list[journeymonitoring_ip_list.index(IP)]
		res = requests.post('http://'+IP+':'+port_to_use+path_to_use, headers = {'Content-type': 'application/xml'}, data=bytearray(XMLJourneyMonitoringTemplate,encoding="utf-8"))
		print("Journey monitoring delivery to: " + str(IP) + " get status: " + str(res.status_code))
  
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
	

