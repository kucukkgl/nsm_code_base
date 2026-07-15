import json
import argparse
import ssl
import socket

def load_roster(path):
    with open(path) as f:
        return json.load(f)

def send_tls12(ip):
    print("Initiating TLS 1.2 handshake with {}:443".format(ip))

    # Create TLS 1.2 context
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # TCP connect
        s = socket.create_connection((ip, 443), timeout=3)

        # Wrap in TLS (ClientHello sent here)
        tls = ctx.wrap_socket(s, server_hostname=ip)

        # Print negotiated version
        print("{}:443 -> Server responded with {}".format(ip, tls.version()))

        tls.close()

    except Exception as e:
        print("{}:443 -> handshake failed ({})".format(ip, e))

def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group '{}' not found".format(group_name))
        return

    group = roster[group_name]
    for student, ip in group.items():
        print("{} -> {}".format(student, ip))
        send_tls12(ip)

def main():
    parser = argparse.ArgumentParser(description="Class TLS 1.2 Launcher (Port 443)")

    parser.add_argument("--roster", default="ids_sec3_students.json",
                        help="Roster JSON file (default: ids_sec3_students.json)")
    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster(args.roster)

    if args.target_ip:
        send_tls12(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
