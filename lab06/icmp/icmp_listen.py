from scapy.all import *

def packet_callback(packet):
    if packet.haslayer(ICMP):
        try:
            print("ICMP Packet Information:")
            print(f"Source IP: {packet[IP].src}")
            print(f"Destination IP: {packet[IP].dst}")
            
            icmp_layer = packet[ICMP]
            print(f"Type: {icmp_layer.type}")
            print(f"Code: {icmp_layer.code}")
            print(f"ID: {icmp_layer.id}")
            print(f"Sequence: {icmp_layer.seq}")
            
            if icmp_layer.payload:
                print(f"Payload: {bytes(icmp_layer.payload)}")
                
            print("=" * 30)
        except Exception as e:
            print(f"Error processing packet: {e}")

def main():
    print("Starting ICMP sniffer...")
    sniff(prn=packet_callback, filter="icmp", store=0)
    
if __name__ == "__main__":
    main()