import argparse
import logging
import os
import socket
import sys
from dotenv import load_dotenv
from telebot import TeleBot


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logging.error("Токен не найден")
    sys.exit(1)

bot = TeleBot(token=TOKEN)

PORTS_TO_SCAN = [22, 3389, 445]


def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except socket.error as e:
        logging.error(f"Ошибка сканирования {ip}:{port} - {e}")
        return False


def scan_ip(ip):
    open_ports = []
    for port in PORTS_TO_SCAN:
        if scan_port(ip, port):
            open_ports.append(str(port))
    return open_ports


def send_notification(ip, open_ports):
    if not open_ports:
        return

    chat_id = os.getenv("CHAT_ID")

    message = f"У сервера {ip} открыты порты:\n" + "\n".join(open_ports)
    bot.send_message(chat_id=chat_id, text=message)
    logging.info(f"Отправлено уведомление для {ip}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Скрипт для сканирования IP-адресов на наличие открытых 22, 3389, 445 портов"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("ip", nargs="?", help="IP для сканирования")
    group.add_argument("-L", "--list", help="Файл со списком IP-адресов")
    return parser.parse_args()


def read_ips_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logging.error(f"Ошибка чтения файла {file_path}: {e}")
        sys.exit(1)


def main():
    args = parse_arguments()

    if args.ip:
        ips = [args.ip]
    else:
        ips = read_ips_from_file(args.list)

    for ip in ips:
        open_ports = scan_ip(ip)
        if open_ports:
            send_notification(ip, open_ports)


if __name__ == "__main__":
    main()
