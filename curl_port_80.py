import json
import argparse
import subprocess

def load_roster(path):
    with open(path) as f:
        return json.load(f)

def curl_ip(ip):
    print("curl http://{}:80".format(ip))
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://{}:80".format(ip)],
            capture_output=True,
            text=True
        )
        print("{} -> HTTP {}".format(ip, result.stdout))
    except Exception as e:
        print("Error contacting {}: {}".format(ip, e))

def attack_group(group_name, roster):
    if group_name not in roster:
        print("Group '{}' not found".format(group_name))
        return

    group = roster[group_name]
    for student, ip in group.items():
        print("{} -> {}".format(student, ip))
        curl_ip(ip)

def main():
    parser = argparse.ArgumentParser(description="Class Curl Launcher")

    parser.add_argument("--roster", default="ids_sec3_students.json",
                        help="Roster JSON file (default: ids_sec3_students.json)")

    parser.add_argument("--target-group", help="Group name (e.g., group1)")
    parser.add_argument("--target-ip", help="Single IP (e.g., 192.168.2.26)")
    args = parser.parse_args()

    roster = load_roster(args.roster)

    if args.target_ip:
        curl_ip(args.target_ip)

    if args.target_group:
        attack_group(args.target_group, roster)

    if not args.target_ip and not args.target_group:
        print("Use --target-group <name> or --target-ip <ip>")

if __name__ == "__main__":
    main()
