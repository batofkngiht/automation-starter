from scapy.all import *
import ipaddress

# Common ports to scan
ports = [25, 80, 53, 443, 445, 8080, 8443]

def SynScan(host):
    """Perform TCP SYN scan on specified ports"""
    try:
        # Send SYN packets and collect responses
        ans, unans = sr(
            IP(dst=host) /
            TCP(sport=33333, dport=ports, flags="S"),
            timeout=2,
            verbose=0
        )
        
        print(f"Open ports at {host}:")
        open_ports = []
        
        for sent, received in ans:
            # Check if it's a SYN-ACK response
            if sent[TCP].dport == received[TCP].sport and received[TCP].flags == "SA":
                open_ports.append(sent[TCP].dport)
                print(f"  Port {sent[TCP].dport} is open")
        
        if not open_ports:
            print("  No open ports found")
            
    except Exception as e:
        print(f"Error during SYN scan: {e}")

def DNSScan(host):
    """Check if host runs a DNS server"""
    try:
        # Send DNS query
        ans, unans = sr(
            IP(dst=host) /
            UDP(dport=53) /
            DNS(rd=1, qd=DNSQR(qname="google.com")),
            timeout=2,
            verbose=0
        )
        
        # Check for DNS response
        if ans:
            for sent, received in ans:
                if received.haslayer(DNS):
                    print(f"DNS Server detected at {host}")
                    return
        else:
            print(f"No DNS response from {host}")
            
    except Exception as e:
        print(f"Error during DNS scan: {e}")

def main():
    """Main function to orchestrate scanning"""
    host = input("Enter IP Address: ").strip()
    
    # Validate IP address
    try:
        ipaddress.ip_address(host)
    except ValueError:
        print("Invalid IP address format")
        exit(-1)
    
    print(f"\nStarting scan for {host}")
    print("-" * 40)
    
    # Perform scans
    SynScan(host)
    print("-" * 40)
    DNSScan(host)
    print("-" * 40)
    print("Scan completed")

if __name__ == "__main__":
    # Important: Run with appropriate permissions
    print("Warning: This script requires root/admin privileges to send raw packets")
    main()