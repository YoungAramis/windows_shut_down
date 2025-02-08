import os
import pyautogui
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import secrets

HOST = ''
PORT = 6669
SECRET = os.getenv('SECRET')



class ShutdownHandler(BaseHTTPRequestHandler):
    """Класс для обработки HTTP запросов."""

    def do_GET(self):
        """Метод для обработки GET запросов."""
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if parsed_path.path == '/shutdown':
            self._handle_secret_check(query_params, 200,
                                      "Компьютер выключается...")

        elif parsed_path.path == '/pause':
            self._handle_secret_check(query_params, 200,
                                      "Клавиша пробел нажата!")

        else:
            self._send_error(404, "Страница не найдена!")

    def _handle_secret_check(self, query_params, status_code, message):
        """Метод для проверки секрета."""
        if "secret" in query_params and query_params["secret"][0] == SECRET:
            self._send_response(status_code, message)
        else:
            self._send_error(403, "Неверный секрет!")

    def _send_response(self, status_code, message):
        """Метод для отправки HTTP ответа."""
        self.send_response(status_code)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"{message}\n".encode("utf-8"))

    def _send_error(self, status_code, message):
        """Метод для отправки HTTP ошибки."""
        self.send_response(status_code)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"{message}\n".encode("utf-8"))


def run_server():
    """Функция для запуска HTTP сервера."""
    server_address = (HOST, PORT)  # Адрес и порт сервера
    httpd = HTTPServer(server_address, ShutdownHandler)  # Создание экземпляра сервера
    print(f"Сервер запущен на порту {PORT}. Жду команд...")  # Вывод сообщения о запуске сервера
    httpd.serve_forever()  # Запуск сервера


if __name__ == '__main__':
    run_server()  # Запуск функции для запуска сервера при выполнении скрипта