#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

import requests

class Messenger:
    def __init__(self, url):
        self.url = url

    def check_service(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return True, "Service is up and running"
            else:
                return False, f"Service is down - Status Code: {response.status_code}"
        except requests.ConnectionError:
            return False, "Failed to connect to the service"

# Usage
messenger = Messenger("http://192.168.0.60:5000/")
#messenger = Messenger("http://0.0.0.0:5000/")
#messenger = Messenger("http://localhost:5000/")
is_ok, message = messenger.check_service()
print(message)
