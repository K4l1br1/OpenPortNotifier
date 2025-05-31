### Использование
Прежде чем использовать скрипт, нужно создать бота в телеграме и добавить в файл .env токен бота, а также id чата. Получить его так: https://api.telegram.org/bot<Токен вашего бота>/getUpdates\
Переменные в .env: TOKEN, CHAT_ID

```
usage: main.py [-h] [-L LIST] [ip]

Скрипт для сканирования IP-адресов на наличие открытых 22, 3389, 445 портов

positional arguments:
  ip                    IP для сканирования

options:
  -h, --help            show this help message and exit
  -L LIST, --list LIST  Файл со списком IP-адресов
```

### Запуск сканирования одного IP
```python .\main.py 127.0.0.1```

### Сканирование серверов из файла
```python .\main.py -L list_of_servers.txt```
