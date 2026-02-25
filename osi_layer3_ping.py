import json
import argparse
from scapy.all import *
import time

def load_roster(path):
    with open(path) as f:
        return json.load(f)

def send_ping(ip, count=10):
    print("Pinging {} ({} times)".format(ip, count))
    pkt = IP(dst=ip)/ICMP()

    # srloop sends the same packet repeatedly
    # inter=0.2 gives a small delay between pings
    srloop(pkt, count=count, inter=0.2, verbose=False)

def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group '{}' not found".format(group_name))
        return

    group = roster[group_name]
    for student, ip in group.items():
        print("{} -> {}".format(student, ip))
        send_ping(ip)

def main():
    parser = argparse.ArgumentParser(description="Class Ping Launcher")

    parser.add_argument("--roster", default="ids_sec3_students.json",
                        help="Roster JSON file (default: ids_sec3_students.json)")

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster(args.roster)

    if args.target_ip:
        send_ping(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
