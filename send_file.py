import json
import sys
import os
import ipaddress
import paramiko

JSON_FILE = "students.json"
REMOTE_DIRECTORY = "/tmp"
CONNECT_TIMEOUT = 5

# Usage:
# python3 send_file.py <file> <password> <username>

if len(sys.argv) != 4:
    print(f"Usage: python3 {sys.argv[0]} <file> <password> <username>")
    print()
    print("Example:")
    print(f"  python3 {sys.argv[0]} passwords.txt 'Pa$$w0rd' administrator")
    sys.exit(1)

LOCAL_FILE = sys.argv[1]
PASSWORD = sys.argv[2]
USERNAME = sys.argv[3]

if not os.path.isfile(LOCAL_FILE):
    print(f"ERROR: File not found: {LOCAL_FILE}")
    sys.exit(1)

try:
    with open(JSON_FILE, "r") as f:
        students = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"ERROR loading {JSON_FILE}: {e}")
    sys.exit(1)

filename = os.path.basename(LOCAL_FILE)
remote_file = f"{REMOTE_DIRECTORY}/{filename}"

successful = []
failed = []
invalid = []

print()
print("=" * 65)
print("Class VM File Distribution")
print("=" * 65)
print(f"File       : {LOCAL_FILE}")
print(f"Username   : {USERNAME}")
print(f"Destination: {remote_file}")
print(f"VM count   : {len(students)}")
print("=" * 65)

for student, ip in students.items():

    ip = ip.strip()

    # Validate IP
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        print(f"[SKIP] {student:20} {ip:16} INVALID IP")
        invalid.append((student, ip))
        continue

    print(f"[SEND] {student:20} {ip:16}", end=" ")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=ip,
            username=USERNAME,
            password=PASSWORD,
            timeout=CONNECT_TIMEOUT,
            banner_timeout=CONNECT_TIMEOUT,
            auth_timeout=CONNECT_TIMEOUT,
            look_for_keys=False,
            allow_agent=False
        )

        sftp = ssh.open_sftp()
        sftp.put(LOCAL_FILE, remote_file)
        sftp.close()

        print("OK")
        successful.append((student, ip))

    except paramiko.AuthenticationException:
        print("AUTH FAILED")
        failed.append((student, ip, "Authentication failed"))

    except (paramiko.SSHException, OSError, TimeoutError) as e:
        print("FAILED")
        failed.append((student, ip, str(e)))

    finally:
        ssh.close()

print()
print("=" * 65)
print("SUMMARY")
print("=" * 65)

print(f"Successful : {len(successful)}")
print(f"Failed     : {len(failed)}")
print(f"Invalid IP : {len(invalid)}")

if failed:
    print("\nFailed machines:")
    for student, ip, reason in failed:
        print(f"  {student:20} {ip:16} {reason}")

if invalid:
    print("\nInvalid IPs:")
    for student, ip in invalid:
        print(f"  {student:20} {ip}")

print("\nFinished.")
