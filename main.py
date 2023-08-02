from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """ Класс, отвечающий за обработку запросов от клиентов """

    def __get_html_content(self):
        """ Метод, получающий html разметку из файла index.html """
        file_path = "index.html"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                return html_content
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
            return None
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None

    def do_GET(self):
        """ Метод, обрабатывающий входящие GET-запросы """
        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)
        page_content = self.__get_html_content()
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(page_content, "utf-8"))


if __name__ == "__main__":
    """ Инициализатор веб-сервера, по заданным параметрам в сети
    принимающий запросы и отправляет их на обработку специальному классу. """
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Способ остановки сервера в консоли через сочетание клавиш Ctrl + C
        pass

    # Остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
