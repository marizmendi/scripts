#! /usr/bin/env python
"""
Ping sweep scan using python
"""
import sys
import os
import ipaddress
import socket
from ping3 import ping

NETWORK = "199.193.137.0/24"
PORT = 80

def tcp(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip,port))
    except ConnectionRefusedError as e:
        print(e)
        pass
    s.close()

def main():
    cidr = ipaddress.ip_network(NETWORK).hosts()
    tcp('192.168.1.1',80)
    for ip in cidr:
        ip = str(ip)
        print(ip)
        tcp(ip,PORT)
        # if ping(str(ip), timeout=0.1):
        #     print(ip)

if __name__ == "__main__":
    main()
