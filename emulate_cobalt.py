from scapy.all import *

target_ip = "192.168.28.27"

# Try resolving the MAC
mac = getmacbyip(target_ip)
if mac is None:
    print(f"Could not resolve MAC for {target_ip}")
    exit()

print(f"Resolved MAC: {mac}")

# Build Ethernet frame manually if needed
eth = Ether(dst=mac)
ip = IP(src="139.155.190.117", dst=target_ip)
udp = UDP(dport=4343)
payload = Raw(load="CobaltStrikePing")

pkt = eth/ip/udp/payload
sendp(pkt)
