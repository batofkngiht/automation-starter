#!/usr/bin/env python3
from scapy.all import *
import os

# ===== CONFIG =====
YOUR_IP = "192.168.100.71"  # CHANGE THIS TO YOUR KALI IP!
REAL_PORTS = [80, 443, 389]     # Fake "real" services
HONEY_PORTS = [2222, 4444, 6666 ,8080]  # Trap ports
# ==================

print(f"[+] HoneyScan starting on {"192.168.100.71"}")
print(f"[+] Real ports (will lie about): {80, 443, 389}")
print(f"[+] Honey ports (will fake open): {2222, 4444, 6666 ,8080}")
print("[+] Waiting for attackers...\n")

blocked_ips = []

def analyze_packet(packet):
    global blocked_ips
    
    # Check if it's a TCP SYN packet
    if packet.haslayer(TCP) and packet[TCP].flags == "S":
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        
        print(f"[Scan] {src_ip} → port {dst_port}", end="")
        
        # Build response packet
        response = IP(dst=packet[IP].src, src=packet[IP].dst) / \
                  TCP(sport=dst_port, dport=packet[TCP].sport, 
                      seq=1000, ack=packet[TCP].seq + 1)
        
        # Decision logic
        if src_ip in blocked_ips:
            if dst_port in REAL_PORTS:
                print(" → LIE (RST) - Telling blocked IP port is closed")
                response[TCP].flags = "RA"  # RST + ACK
                send(response, verbose=0)
            elif dst_port in HONEY_PORTS:
                print(" → TRAP (SYN/ACK) - Fake welcome!")
                response[TCP].flags = "SA"  # SYN + ACK
                send(response, verbose=0)
            else:
                print(" → Ignoring")
        else:
            # New IP
            if dst_port not in REAL_PORTS:
                print(f" → NEW ATTACKER! Adding {src_ip} to block list")
                blocked_ips.append(src_ip)
                
                if dst_port in HONEY_PORTS:
                    print("   + Sending honeypot response")
                    response[TCP].flags = "SA"
                    send(response, verbose=0)
            else:
                print(" → Legitimate service request (allowing)")

# Start sniffing
filter_str = f"dst host {"192.168.100.71"} and tcp"
sniff(filter=filter_str, prn=analyze_packet, store=0)