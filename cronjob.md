Check what python3 points to:
readlink -f /usr/bin/python3


Expected:

/usr/bin/python3.5

Grant raw-socket permission to Python:
sudo setcap cap_net_raw+ep /usr/bin/python3.5

Verify it worked:
getcap /usr/bin/python3.5


Expected:

/usr/bin/python3.5 = cap_net_raw+ep

Test the script manually without sudo:
/usr/bin/python3 /home/student/nsm_code_base/osi_layer4_tcp_port80.py --roster /home/student/nsm_code_base/ids_fall26.json --target-group group1


Make sure you do not see:

Operation not permitted

Edit your user crontab:
crontab -e

Add this entry (runs at 10 AM, 2 PM, 6 PM, and 10 PM and prepends a timestamp to the log):
0 10,14,18,22 * * * date >> /home/student/80_1.log; /usr/bin/python3 /home/student/nsm_code_base/osi_layer4_tcp_port80.py --roster /home/student/nsm_code_base/ids_fall26.json --target-group group1 >> /home/student/80_1.log 2>&1

Save and exit.
