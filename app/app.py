from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Логирует каждый запрос в stdout вместо stderr по умолчанию
        sys.stdout.write("%s - - [%s] %s\n" % (self.client_address[0], self.log_date_time_string(), format%args))
        sys.stdout.flush()

    def do_GET(self):
        if self.path == '/':
            self.send_json_response({"name": "my-minimal-http-service"})
        elif self.path == '/health':
            self.send_json_response({"status": "ok"})
        else:
            self.send_json_response({"error": "Not Found"}, status=404)

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run(port=8000):
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Сервер запущен на порту {port}...", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.", flush=True)
        httpd.server_close()

if __name__ == '__main__':
    run()
