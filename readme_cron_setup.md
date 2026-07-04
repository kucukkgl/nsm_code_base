# Cron Setup for Scapy-Based Ping Launcher

This project uses a Python script (with Scapy) to send ICMP packets to student endpoints.  
Because Scapy relies on **raw sockets**, special permissions are required for the script to run correctly under cron.

This README explains:
- why raw sockets normally require root,
- why cron fails when `sudo` is used,
- how to grant Python the correct capability,
- and how to configure the working cron job.

---

## Why Raw Sockets Require Root

Linux protects raw sockets because they allow direct packet crafting at OSI Layer 3.  
Operations such as:

- creating raw sockets  
- sending custom ICMP packets  
- modifying packet headers  

require the privileged capability **CAP_NET_RAW**.

By default, only the **root** user has this capability.  
This is why the script works when run manually with:


but fails under cron.

---

## Why Cron Fails When `sudo` Is Present

Cron runs in a **non-interactive environment** with:

- no terminal (TTY),
- no password prompt,
- no graphical askpass helper.

So any cron job containing `sudo` will fail with:



Even after granting Python raw-socket capability, **any leftover sudo** (in the cron line or inside the script) will break the job.

---

## Solution: Grant Python the Raw Socket Capability

Instead of running the entire cron job as root, grant Python the specific capability it needs:

### 1. Identify the real Python binary
```bash
ls -l /usr/bin/python3
sudo setcap cap_net_raw+ep /usr/bin/python3.5
getcap /usr/bin/python3.5


crontab -e
*/3 * * * * /usr/bin/python3 /home/student/nsm_code_base/osi_layer3_ping.py \
  --roster /home/student/nsm_code_base/ids/summer26.json \
  --target-group group1 >> /home/student/custom_cron.log 2>&1
