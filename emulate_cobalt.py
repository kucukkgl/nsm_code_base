from scapy.all import *

target_ip = "192.168.28.0/24"

# Build Ethernet frame manually if needed
eth = Ether(dst=mac)
ip = IP(src="139.155.190.117", dst=target_ip)
udp = UDP(dport=4343)
payload = Raw(load="CobaltStrikePing")

pkt = eth/ip/udp/payload
sendp(pkt)
