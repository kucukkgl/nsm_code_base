from scapy.all import *

ip = IP(dst="192.168.28.27")
tcp = TCP(dport=80, sport=RandShort(), flags="PA", seq=1000)
http = (
    'GET / HTTP/1.1\r\n'
    'Host: TARGET_HOST\r\n'
    'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)\r\n'
    'Accept: */*\r\n'
    '\r\n'
)

packet = ip/tcp/http
send(packet)
