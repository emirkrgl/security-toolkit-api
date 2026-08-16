from scapy.all import ARP, Ether, srp
import socket
def get_hostname(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.herror:
        return "bilinmiyor"
def run(target_network, timeout=3):
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_network)
    try:
        result = srp(packet, timeout=timeout, verbose=False, inter=0.1)[0]
        cihaz_listesi = []
        for sent, received in result:
            name = get_hostname(received.psrc)

            cihaz_listesi.append({
                "ip": received.psrc,
                "mac": received.hwsrc,
                "hostname": name,
            })
        return cihaz_listesi
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []