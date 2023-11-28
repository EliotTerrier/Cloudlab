#!/usr/bin/env python3


import argparse
import logging
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

# Callback that will be called whenever the state of a service changes.
# The state changes can be ServiceStateChange.Added, ServiceStateChange.Removed, or ServiceStateChange.Updated

def on_service_state_change(
    zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    services = ["_http._tcp.local."] # list of services to browse for

    zeroconf = Zeroconf() # creates a Zeroconf instance, starts browsing for the specified services

    print("\nBrowsing %d service(s), press Ctrl-C to exit...\n" % len(services))
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
