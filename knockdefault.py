#!/usr/bin/python

from scapy.all import *
import sys
import os
import time

def knockd_test(ip,start_key):
        ##print "\n[-] Sending default knockd sequence to " + ip
	for x in start_key:
                send(IP(dst=ip)/TCP(dport=x),verbose=0)
	time.sleep(2)
	for x in start_key:
                send(IP(dst=ip)/TCP(dport=x),verbose=0)

	## Subsequent Nmap Scan
	os.system('nmap -vvv -p 22,80 10.11.1.xxx')

## Default start and stop knockd port knock sequences
start_key = (7,2350,43)

## Execution of function
knockd_test("10.11.1.xxx",start_key)
