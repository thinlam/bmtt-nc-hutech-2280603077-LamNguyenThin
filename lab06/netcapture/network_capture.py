import sys
import io
import subprocess
from scapy.all import *
from threading import Thread

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def get_interfaces():
    result = subprocess.run(["netsh", "interface", "show", "interface"], 
                          capture_output=True, text=True, encoding='utf-8')
    interfaces = []
    for line in result.stdout.splitlines()[3:]:
        parts = line.split()
        if len(parts) >= 4:
            interfaces.append(parts[3])
    return interfaces

def packet_handler(packet):
    if packet.haslayer(TCP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        sport = packet[TCP].sport
        dport = packet[TCP].dport
        
        print(f"\n[TCP Packet] {src_ip}:{sport} -> {dst_ip}:{dport}")
        
        if packet.haslayer(Raw):
            payload = packet[Raw].load[:100]
            print(f"Payload (100 bytes đầu): {payload}")

def main():
    interfaces = get_interfaces()
    
    print("Danh sách giao diện mạng:")
    for i, iface in enumerate(interfaces, start=1):
        print(f"{i}. {iface}")
    
    try:
        choice = int(input("Chọn giao diện mạng (nhập số): "))
        selected_iface = interfaces[choice - 1]
        
        print(f"\nBắt đầu bắt gói tin trên {selected_iface}...")
        
        # Chạy sniff trong thread riêng
        sniff_thread = Thread(target=sniff, kwargs={
            'iface': selected_iface,
            'prn': packet_handler,
            'filter': "tcp"
        })
        sniff_thread.daemon = True
        sniff_thread.start()
        
        input("Nhấn Enter để dừng...\n")
        
    except (ValueError, IndexError):
        print("Lựa chọn không hợp lệ!")
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()