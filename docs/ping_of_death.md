# Ping of Death - Teaching Guide

Purpose: short lab guide to detect the `ping_of_death.py` exercise with Snort and Wireshark in a controlled environment.

Files added:
- rules/ping_of_death.rules — simple Snort content rule (SID 1000001).

Snort rule (already added):
```
alert icmp any any -> any any (msg:"PING_OF_DEATH script - repeated X in ICMP payload"; content:"XXXXXXXX"; depth:64; classtype:attempted-dos; sid:1000001; rev:1;)
```

Include the rule: add an include line to your `snort.conf` rules section, e.g.
```
include $RULE_PATH/ping_of_death.rules
```

Run Snort (example):
```bash
sudo snort -c /etc/snort/snort.conf -A console -q -i <interface>
```

Start capture in Wireshark (or open the live interface). Useful display filters:
- Show IP fragments: `ip.flags.mf == 1 || ip.frag_offset > 0`
- Show ICMP fragments and reassembly artifacts: `icmp || (ip.flags.mf == 1 || ip.frag_offset > 0)`
- Search payload bytes (teaching only): `frame contains "XXXXXXXX"`

tcpdump command to capture to a pcap for later analysis:
```bash
sudo tcpdump -i <interface> -w ping_of_death.pcap "icmp or (ip[6:2] & 0x1fff != 0)"
```

Snort reassembly/fragmentation hardening (suggested teaching config snippets):
```
# in snort.conf (frag3 preprocessor)
preprocessor frag3_global: max_frags 65536
preprocessor frag3_engine: policy linux detect_anomalies, overlap_limit 10, tiny_frag_limit 2
```

Test steps (controlled lab only):
1. Start Snort on the monitoring host.  
2. Start Wireshark/tcpdump on the same or another monitoring host.  
3. From the attacker VM run: `sudo python3 ping_of_death.py <target-vm-ip>`
4. Watch Snort console for SID 1000001 and examine the pcap/Wireshark display filters for fragmentation and the repeated-`X` payload.

Tuning notes:
- The provided rule is intentionally simple for teaching and may generate false positives if legitimate ICMP contains repeated `X` bytes.  
- For stronger detection, combine content checks with fragment/reassembly anomaly detection (see frag3).  
- Use experimental SID ranges (>=1000000) in class labs.

Safety: Do not run this outside isolated lab networks or without explicit permission.
