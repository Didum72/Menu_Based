#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import urllib.parse
import os

save_dir = "/path/to/save/directory"

class ClickPhotoHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_data = urllib.parse.parse_qs(post_data)
        
        image_data = post_data.get('image', [None])[0]

        if image_data:
            success, message = self.save_image(image_data)
            if success:
                self.respond(200, "<h1>Photo saved successfully!</h1>")
            else:
                self.respond(500, f"<h1>Error: {message}</h1>")
        else:
            self.respond(400, "<h1>No image data received.</h1>")

    def save_image(self, image_data):
        try:
            # Decode the base64 image data
            image_data = base64.b64decode(image_data.split(',')[1])
            # Generate a unique filename
            filename = os.path.join(save_dir, "photo.png")
            # Save the image
            with open(filename, "wb") as f:
                f.write(image_data)
            return True, "Image saved successfully."
        except Exception as e:
            return False, str(e)

    def respond(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=ClickPhotoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
