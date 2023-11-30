from zeroconf import Zeroconf, ServiceBrowser, ServiceListener
import time
import socket

class ServiceMonitor(ServiceListener):
    def __init__(self, desired_service, condition):
        super().__init__()
        self.inf = {}
        self.desired_service = desired_service
        self.condition = condition
        
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        self.inf[name] = info
        print(f"MONITOR - {time.strftime('%H:%M:%S',)} Service {name} updated, service info: {info}")
        with self.condition:
            self.condition.notify_all()
    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"MONITOR - {time.strftime('%H:%M:%S',)} Service {name} removed, service info: {info}")
        if name in self.inf:
            del self.inf[name]       
        with self.condition:
            self.condition.notify_all()
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        
        if self.desired_service not in name:
            return
        info = zc.get_service_info(type_, name)
        self.inf[name] = info
        print(f"MONITOR - {time.strftime('%H:%M:%S',)} Service {name} added, service info: {info}")
        ip_address_str = socket.inet_ntoa(info.addresses[0])
        print(f"IP address: {ip_address_str}")
        with self.condition:
            self.condition.notify_all()

    # Similar modifications for remove_service and update_service

    def getInfo(self):
        return self.inf

