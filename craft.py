from scapy.all import *

pkt = IP(dst="192.168.28.27")/TCP(dport=80, flags="S")/Raw(load="GET /evil.php HTTP/1.1\r\nHost: test.com\r\n\r\n")
send(pkt)

