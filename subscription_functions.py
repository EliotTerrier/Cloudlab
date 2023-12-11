import xml.etree.ElementTree as ET
from flask import Response, request
import requests

def subscription_request(service_ip, service_port, path, operation_name, server_ip, server_port, reply_path):
    subscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <SubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>{reply_path}</ReplyPath>
    </SubscribeRequest>"""
    print(subscription_request)

    response = requests.post(f'http://{service_ip}:{service_port}/{path}{operation_name}', headers = {'Content-Type': 'application/xml'}, data=subscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses

def unsubscription_request(service_ip, service_port, path, operation_name, server_ip, server_port, reply_path):
    unsubscription_request = f"""<?xml version="1.0" encoding="utf-8"?>
    <UnsubscribeRequest>
        <Client-IP-Address>{server_ip}</Client-IP-Address>
        <ReplyPort>{server_port}</ReplyPort>
        <ReplyPath>{reply_path}</ReplyPath>
    </UnsubscribeRequest>"""
    print(unsubscription_request)

    response = requests.post(f'http://{service_ip}:{service_port}/{path}{operation_name}', headers = {'Content-Type': 'application/xml'}, data=unsubscription_request)
    response.raise_for_status()  # Raises HTTPError for bad responses
    
def handle_subscription(ip_list, port_list, path_list):

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
						if client_ip in ip_list:
							port_list[ip_list.index(client_ip)]=reply_port
							path_list[ip_list.index(client_ip)]=reply_path
						else:
							ip_list.append(client_ip)
							port_list.append(reply_port)
							path_list.append(reply_path)
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
						if client_ip in ip_list:
							ind = ip_list.index(client_ip)
							del ip_list[ind]
							del port_list[ind]
							del path_list[ind]
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
	
def daemon(ip_list, port_list, path_list, XMLTemplate):
    for IP in ip_list:
        port_to_use = port_list[ip_list.index(IP)]
        path_to_use = path_list[ip_list.index(IP)]
        res = requests.post('http://' + IP + ':' + port_to_use + path_to_use, headers={'Content-type': 'application/xml'}, data=bytearray(XMLTemplate, encoding="utf-8"))
        print("Delivery to: " + str(IP) + " get status: " + str(res.status_code))