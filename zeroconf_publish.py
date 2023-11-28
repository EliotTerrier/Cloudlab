#!/usr/bin/env python3

from time import sleep
from zeroconf import ServiceInfo, Zeroconf
import socket

if __name__ == '__main__':
    
    # Service information definition
    desc = {
        'txtvers': '1',
        'version': '2.1.1',
        'model': 'model26',
        'manufacturer': 'ITxPT',
        'serialnumber': 'SN0123456789',
        'softwareversion': 'v1.2.3',
        'hardwareversion': 'revision D',
        'macaddress': 'CF:DA:98:63:9D:F6',
        'status': '0',
        'services': 'inventory;avms'
    }
    info = ServiceInfo(
        "_http._tcp.local.",
        "Nobino-inventory._http._tcp.local.",
        addresses=['10.0.9.227'],
        port=9,
        
        properties=desc,  # The TXT record is added here
    )

    # Zeroconf configuration
    zeroconf = Zeroconf()

    print("Registration of a service, press Ctrl-C to exit...")

    # Register the service
    zeroconf.register_service(info)

    try:
        # Main loop
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

