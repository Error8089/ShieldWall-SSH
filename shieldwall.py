import time
import os
import re
import subprocess

# Настройки для Fedora
LOG_FILE = "/var/log/secure"
THRESHOLD = 5  # Бан после 5 попыток

def ban_ip(ip):
    print(f"🛑 Блокирую нарушителя: {ip}")
    # Команда для Fedora Firewall
    subprocess.run(["sudo", "firewall-cmd", "--add-rich-rule", f'rule family="ipv4" source address="{ip}" reject'])

def monitor():
    print("🛡️ ShieldWall активен. Слежу за /var/log/secure...")
    # Открываем лог
    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END) # Прыгаем в конец файла
        attempts = {}
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            # Ищем ошибки входа SSH
            if "Failed password" in line:
                ip = re.search(r"from ([\d\.]+) port", line).group(1)
                attempts[ip] = attempts.get(ip, 0) + 1
                print(f"⚠️ Неудачный вход с {ip} ({attempts[ip]}/{THRESHOLD})")
                
                if attempts[ip] >= THRESHOLD:
                    ban_ip(ip)
                    attempts[ip] = 0

if __name__ == "__main__":
    monitor()
