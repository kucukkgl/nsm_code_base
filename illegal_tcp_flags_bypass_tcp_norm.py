#!/usr/bin/env python3
import argparse
from scapy.all import *

# -----------------------------
# Parse command-line arguments
# -----------------------------
parser = argparse.ArgumentParser(description="Send illegal TCP flag combination")
parser.add_argument("-dst", required=True, help="Destination IP address")
args = parser.parse_args()

dst_ip = args.dst

# -----------------------------
# Send illegal TCP flags (SYN+FIN)
# -----------------------------
print(f"[+] Sending illegal TCP flags to {dst_ip}")

pkt = IP(dst=dst_ip) / TCP(dport=80, flags="SF")
send(pkt, verbose=0)

print("[+] Packet sent.")
