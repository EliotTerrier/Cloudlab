#!/usr/bin/env python3


import argparse
import logging
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

# Callback that will be called whenever the state of a service changes.
# The state changes can be ServiceStateChange.Added, ServiceStateChange.Removed, or ServiceStateChange.Updated

def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:
    print(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name) #retrieves the service info
        print("Info from zeroconf.get_service_info: %r" % (info))

        if info: #If service info available, prints the addresses (IP and port) and the server
            addresses = ["%s:%d" % (addr, int(info.port)) for addr in info.parsed_scoped_addresses()]
            print("  Addresses: %s" % ", ".join(addresses))
            print(f"  Server: {info.server}")
        else:
            print("  No info")
        print('\n')

def browse_service(service_type):
    # In this case, the logging level is set to INFO, which means the logger will handle all messages with a severity of INFO and above.
    logging.basicConfig(level=logging.INFO)

    zeroconf = Zeroconf()
    print(f"\nBrowsing service {service_type}, press Ctrl-C to exit...\n")
    
    # A new instance of ServiceBrowser is created. ServiceBrowser is a class for browsing services on a network.
    # The ServiceBrowser takes three arguments: a Zeroconf instance, a list of service types to look for, and a list of callback functions to call when a service of the specified type is found or lost.
    # In this case, the callback function is on_service_state_change, which will be called whenever a service is added or removed.
    browser = ServiceBrowser(zeroconf, [service_type], handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
        
    return zeroconf, browser
