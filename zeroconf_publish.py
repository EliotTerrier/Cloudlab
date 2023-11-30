#!/usr/bin/env python3

from time import sleep
from zeroconf import ServiceInfo, Zeroconf
import socket


def publish_service(name, service_type, ipaddress, port, properties):
    #global exit_program
    info = ServiceInfo(
        service_type,
        f"{name}.{service_type}",
        addresses=[socket.inet_aton(ipaddress)],
        port=port,
        properties=properties,
    )

    zeroconf = Zeroconf()
    print(f"Registration of a service {name}, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
     # Main loop
        while True: #not exit_program:
            sleep(0.1)
            
    except KeyboardInterrupt: #except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        # Cleanup
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

    





