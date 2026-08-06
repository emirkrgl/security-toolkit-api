import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
def banner_ayikla(ham_veri):
    if not ham_veri:
        return "Cevap yok (Sessiz Servis)"
    try:
        metin = ham_veri.decode(errors='ignore').strip()
        if "HTTP" in metin:
            for satir in metin.split('\r\n'):
                if "Server:" in satir:
                    return satir.replace("Server:", "").strip()
            return "Web Sunucusu (Detay yok)"
        return metin.replace('\n', ' ').replace('\r', '')[:50]
    except Exception:
        return "Veri okunamadı"


def port_tara(target,port,connect_timeout=0.5, response_timeout=1.5, verbose=False):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(connect_timeout)
        result = s.connect_ex((target, port))

        if result == 0:
            if port in [80, 8080, 443]:
                payload = b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n"
            elif port == 3306:
                payload = b"\x00\x00\x00\x01\x00"
            elif port in [21, 22]:
                payload = None
            else:
                payload = b"\r\n"
            try:
                port_servis = socket.getservbyport(port)
            except Exception:
                port_servis = "bilinmeyen"

            ceviri_cevap = "Cevap yok"
            try:
                s.settimeout(response_timeout)
                if payload:
                    s.send(payload)
                gelen = s.recv(1024)
                ceviri_cevap = banner_ayikla(gelen)
            except Exception:
                pass
            if verbose:
                print(
                    f"{Fore.GREEN}[+] Port {port:5}: AÇIK{Style.RESET_ALL} "
                    f"{port_servis:15} CEVAP-> {ceviri_cevap}\n"
                )
            s.close()
            return {"port": port, "service": port_servis, "banner": ceviri_cevap}
        s.close()
        return None
    except Exception:
        return None

def run(target, start_port, end_port, connect_timeout=0.5, response_timeout=1.5, verbose=True):
    try:
        futures = []
        results = []
        socket.gethostbyname(target)  # verilen domain adresini ip adresine çeviren fonksiyon
        with ThreadPoolExecutor(max_workers=10) as executor:
            for port in range(start_port, end_port):
                sonuc = executor.submit(
                    port_tara, target, port, connect_timeout, response_timeout, verbose
                )
                futures.append(sonuc)
            for f in futures:
                tarama_sonucu = f.result()
                if tarama_sonucu is not None:
                    results.append(tarama_sonucu)
        return results
    except socket.gaierror:
        print("Hata: Geçersiz adres!")
    except ValueError:
        print("Hata: Portlar sayı olmalıdır!")
    except KeyboardInterrupt:
        print("\nDurduruldu.")