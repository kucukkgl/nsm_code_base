import sys
from scapy.all import *

def send_malicious_handshake(victim_ip):
 # create objects using  Ether() IP() and TCP() constructors
 ip = IP(dst=victim_ip)
 tcp = TCP(dport=80, sport=RandShort(), seq=1000, flags="S")

 # send ip/tcp and wait until you get synack from victim
 synack= sr1(ip/tcp, timeout=5)
 
 #print("capture SYN/ACK and produce ACK")
 tcp_ack = TCP(dport=80, sport=tcp.sport, seq=synack.ack, ack=synack.seq+1, flags="A")

 send(ip/tcp_ack)



if __name__ == "__main__":
 victim_ip = sys.argv[1]
 send_malicious_handshake(victim_ip)

 


