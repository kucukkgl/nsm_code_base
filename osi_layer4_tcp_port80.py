import json
import argparse
from scapy.all import *

def load_roster(path):
    with open(path) as f:
        return json.load(f)

def send_tcp_80(ip):
    print("Sending TCP SYN to {}:80".format(ip))
    pkt = IP(dst=ip)/TCP(dport=80, flags="S")

    # sr1 sends one packet and waits for one response
    try:
        resp = sr1(pkt, timeout=2, verbose=False)
        if resp is None:
            print("{}:80 -> no response".format(ip))
        else:
            print("{}:80 -> got {}".format(ip, resp.summary()))
    except Exception as e:
        print("Error contacting {}: {}".format(ip, e))

def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group '{}' not found".format(group_name))
        return

    group = roster[group_name]
    for student, ip in group.items():
        print("{} -> {}".format(student, ip))
        send_tcp_80(ip)

def main():
    parser = argparse.ArgumentParser(description="Class TCP Port 80 Launcher (Scapy)")

    parser.add_argument("--roster", default="ids_sec3_students.json",
                        help="Roster JSON file (default: ids_sec3_students.json)")
    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster(args.roster)

    if args.target_ip:
        send_tcp_80(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
