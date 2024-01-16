# 基于 Qt5 + http.server GUI 支持

import http.server
import socketserver

PORT = 6180
FILE_TO_SERVE = 'your_file.html'  # 指定要提供的文件路径和文件名

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        with open(FILE_TO_SERVE, 'rb') as file:
            self.wfile.write(file.read())

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print("Server running at port", PORT)
    httpd.serve_forever()