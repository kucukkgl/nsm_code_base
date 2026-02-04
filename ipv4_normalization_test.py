#!/usr/bin/env python3

"""
This script is part of the NSM code base and is used to demonstrate how
Snort's IPv4 normalization preprocessor (normalize_ip4) behaves when it
encounters malformed IPv4 packets.

The goal:
    - Craft an intentionally malformed IPv4 packet
    - Send it to a Snort sensor
    - Observe how Snort handles it with and without the normalize_ip4 preprocessor

Why this matters:
    Attackers often send packets that the OS accepts but the IDS rejects.
    Normalization preprocessors remove this ambiguity by rewriting malformed
    headers into a canonical form before detection rules run.
"""

import argparse
from scapy.all import IP, Raw, send

def main():
    parser = argparse.ArgumentParser(
        description="Send a malformed IPv4 packet to test Snort's normalize_ip4 preprocessor"
    )
    parser.add_argument(
        "-dst",
        required=True,
        help="Destination IP address (the host monitored by Snort)"
    )
    args = parser.parse_args()

    # -------------------------------------------------------------
    # Payload that we want Snort to detect.
    # If normalization works, Snort should still see this payload
    # even though the IPv4 header is intentionally incorrect.
    # -------------------------------------------------------------
    payload = b"EVASIONTEST"

    # -------------------------------------------------------------
    # MALFORMED IPv4 PACKET
    #
    # We set the IPv4 'len' field to 20 bytes, which is the size of
    # the IPv4 header alone. However, we ALSO attach a payload.
    #
    # This creates a mismatch:
    #   - Header claims: "This packet is only 20 bytes long"
    #   - Actual packet: header (20 bytes) + payload (11 bytes)
    #
    # This is a classic IDS evasion technique.
    #
    # Snort behavior:
    #   WITHOUT normalize_ip4:
    #       Snort may drop or ignore the packet because the header is invalid.
    #
    #   WITH normalize_ip4:
    #       Snort rewrites the 'len' field to the correct value,
    #       allowing detection rules to inspect the payload normally.
    # -------------------------------------------------------------
    pkt = IP(dst=args.dst, len=20) / Raw(payload)

    print(f"[+] Sending malformed IPv4 packet to {args.dst}")
    print("[+] This packet intentionally violates the IPv4 total length field")
    print("[+] Use this to test Snort's normalize_ip4 preprocessor behavior")

    # -------------------------------------------------------------
    # Send the packet on the wire.
    # Raw sockets require root privileges, so run with sudo.
    # -------------------------------------------------------------
    send(pkt)

if __name__ == "__main__":
    main()
