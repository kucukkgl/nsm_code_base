from scapy.all import *
cobalt_ips=["139.155.190.117", "168.61.180.98","23.224.152.138", "104.243.41.123", "106.55.153.204", "165.27.85.160", "167.99.197.196"]

target_ip = "192.168.28.27"

pkt=IP(src=cobalt_ips[0],dst=target_ip) / UDP(dport=4343) / Raw(load="CobaltStrikePing")
send(pkt)
