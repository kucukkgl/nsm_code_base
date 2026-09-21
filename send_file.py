import argparse
import json
import os
import ipaddress
import paramiko

JSON_FILE = "students.json"
REMOTE_DIRECTORY = "/tmp"
CONNECT_TIMEOUT = 5


# --------------------------------------------------
# Command-line arguments
# --------------------------------------------------

parser = argparse.ArgumentParser(
    description="Send a file to student lab VMs."
)

parser.add_argument(
    "--file",
    required=True,
    help="Local file to send"
)

parser.add_argument(
    "--username",
    required=True,
    help="Username on the recipient VMs"
)

parser.add_argument(
    "--password",
    required=True,
    help="Password on the recipient VMs"
)

args = parser.parse_args()

LOCAL_FILE = args.file
USERNAME = args.username
PASSWORD = args.password


# --------------------------------------------------
# Check file
# --------------------------------------------------

if not os.path.isfile(LOCAL_FILE):
    print(f"ERROR: File not found: {LOCAL_FILE}")
    raise SystemExit(1)


# --------------------------------------------------
# Load students
# --------------------------------------------------

try:
    with open(JSON_FILE, "r") as f:
        students = json.load(f)

except FileNotFoundError:
    print(f"ERROR: {JSON_FILE} not found.")
    raise SystemExit(1)

except json.JSONDecodeError as e:
    print(f"ERROR: Invalid JSON: {e}")
    raise SystemExit(1)


filename = os.path.basename(LOCAL_FILE)
remote_file = f"{REMOTE_DIRECTORY}/{filename}"

successful = []
failed = []
invalid = []


# --------------------------------------------------
# Send file
# --------------------------------------------------

for student, ip in students.items():

    ip = ip.strip()

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

        sftp.put(
            LOCAL_FILE,
            remote_file
        )

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


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Successful : {len(successful)}")
print(f"Failed     : {len(failed)}")
print(f"Invalid IP : {len(invalid)}")

if failed:
    print("\nFailed VMs:")

    for student, ip, reason in failed:
        print(f"  {student:20} {ip:16} {reason}")

if invalid:
    print("\nInvalid IPs:")

    for student, ip in invalid:
        print(f"  {student:20} {ip}")

print("\nFinished.")
