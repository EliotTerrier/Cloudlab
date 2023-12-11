# Virtual environment ITxPT laboratory project repository
This is the repository about the ITxPT cloudlab project, the current situation of it is that there is a avms service up and running and a client can subscribe and get data from it. Same for gnsslocation service.

# Utilisation

- **Simulate AVMS service**: run `itxpt_avms.py` & `client_consumer.py` in 2 different terminals

- **Simulate gnsslocation service**: run `itxpt_gnsslocation.py` and `gnsslocation_client.py` on 2 different devices

# Structure

| File                   | Description                                                  |
|------------------------|--------------------------------------------------------------|
| **itxpt_avms.py**      | Simulation of an AVMS service to handle subscription from a client and send data to it.                                    |
| **client_consumer.py** | Simulation of a client subscribing to the AVMS service.        |
| **itxpt_gnsslocation** | Simulation of a GNSS location service.                         |
| **gnsslocation_client.py** | Simulation of a device subscribing to the GNSS location service. |
| **Data.py**            | AVMS & GNSSlocation static data used in the scripts.        |
| **itxpt_inventory**    | Simulation of an inventory service.                            |
| **service_discovery.py**| Library used for service discovery features.                  |
| **subscription_function.py** | Library used for subscription handling and sending data features.|

