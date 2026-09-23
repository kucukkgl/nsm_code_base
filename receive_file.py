import argparse
import json
import os
import ipaddress
import paramiko


CONNECT_TIMEOUT = 5
OUTPUT_DIRECTORY = "/home/administrator"


# --------------------------------------------------
# Command-line arguments
# --------------------------------------------------

parser = argparse.ArgumentParser(
    description="Download a file from student lab VMs."
)

parser.add_argument(
    "--recipients",
    required=True,
    help="JSON file containing student names and IP addresses"
)

parser.add_argument(
    "--remote-file",
    required=True,
    help="Full path of the file to download from each VM"
)

parser.add_argument(
    "--username",
    required=True,
    help="Username on the student VMs"
)

parser.add_argument(
    "--password",
    required=True,
    help="Password on the student VMs"
)

args = parser.parse_args()


JSON_FILE = args.recipients
REMOTE_FILE = args.remote_file
USERNAME = args.username
PASSWORD = args.password


# --------------------------------------------------
# Check output directory
# --------------------------------------------------

if not os.path.isdir(OUTPUT_DIRECTORY):
    print(f"ERROR: Output directory not found: {OUTPUT_DIRECTORY}")
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


# --------------------------------------------------
# Get remote filename
# --------------------------------------------------

filename = os.path.basename(REMOTE_FILE)

if not filename:
    print("ERROR: Remote file path does not contain a filename.")
    raise SystemExit(1)


# --------------------------------------------------
# Result lists
# --------------------------------------------------

successful = []
failed = []
not_found = []
invalid = []


# --------------------------------------------------
# Download file from each VM
# --------------------------------------------------

for student, ip in students.items():

    ip = ip.strip()


    # --------------------------------------------------
    # Validate IP address
    # --------------------------------------------------

    try:
        ipaddress.ip_address(ip)

    except ValueError:
        print(f"[SKIP] {student:20} {ip:16} INVALID IP")
        invalid.append((student, ip))
        continue


    print(f"[GET ] {student:20} {ip:16}", end=" ")


    # --------------------------------------------------
    # Create SSH client
    # --------------------------------------------------

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )


    try:

        # --------------------------------------------------
        # Connect using SSH
        # --------------------------------------------------

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


        # --------------------------------------------------
        # Open SFTP connection
        # --------------------------------------------------

        sftp = ssh.open_sftp()


        # --------------------------------------------------
        # Make student name safe for local filename
        # --------------------------------------------------

        safe_student = "".join(
            c if c.isalnum() or c in "-_" else "_"
            for c in student
        )


        # --------------------------------------------------
        # Create local filename
        #
        # Example:
        #
        # john.pot_Alice_downloaded.txt
        # john.pot_Bob_downloaded.txt
        #
        # --------------------------------------------------

        local_file = os.path.join(
            OUTPUT_DIRECTORY,
            f"{filename}_{safe_student}_downloaded.txt"
        )


        # --------------------------------------------------
        # Download file
        # --------------------------------------------------

        try:

            sftp.get(
                REMOTE_FILE,
                local_file
            )

            print("OK")

            successful.append(
                (student, ip, local_file)
            )


        # --------------------------------------------------
        # Remote file does not exist
        # --------------------------------------------------

        except FileNotFoundError:

            print("FILE NOT FOUND")

            not_found.append(
                (student, ip)
            )


        finally:

            sftp.close()


    # --------------------------------------------------
    # Authentication failure
    # --------------------------------------------------

    except paramiko.AuthenticationException:

        print("AUTH FAILED")

        failed.append(
            (student, ip, "Authentication failed")
        )


    # --------------------------------------------------
    # SSH / network failure
    # --------------------------------------------------

    except (paramiko.SSHException, OSError, TimeoutError) as e:

        print("FAILED")

        failed.append(
            (student, ip, str(e))
        )


    finally:

        ssh.close()


# --------------------------------------------------
# Summary
# --------------------------------------------------

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Downloaded : {len(successful)}")
print(f"Not found  : {len(not_found)}")
print(f"Failed     : {len(failed)}")
print(f"Invalid IP : {len(invalid)}")


# --------------------------------------------------
# Successful downloads
# --------------------------------------------------

if successful:

    print("\nDownloaded files:")

    for student, ip, local_file in successful:

        print(
            f"  {student:20} "
            f"{ip:16} -> {local_file}"
        )


# --------------------------------------------------
# Files not found
# --------------------------------------------------

if not_found:

    print("\nFiles not found:")

    for student, ip in not_found:

        print(
            f"  {student:20} "
            f"{ip:16} "
            f"{REMOTE_FILE}"
        )


# --------------------------------------------------
# Failed connections
# --------------------------------------------------

if failed:

    print("\nFailed VMs:")

    for student, ip, reason in failed:

        print(
            f"  {student:20} "
            f"{ip:16} "
            f"{reason}"
        )


# --------------------------------------------------
# Invalid IP addresses
# --------------------------------------------------

if invalid:

    print("\nInvalid IPs:")

    for student, ip in invalid:

        print(
            f"  {student:20} "
            f"{ip}"
        )


print("\nFinished.")
