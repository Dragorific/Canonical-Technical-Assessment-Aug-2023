from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonschema import validate, ValidationError
from Event import *
from EventStorage import *
from schemas import event_schema

AUTH_TOKEN = "secret_token"  # Simple authentication token

class AuditLogHandler(BaseHTTPRequestHandler):
    storage = EventStorage()

    def do_POST(self):
        if self.headers.get("Authorization") != AUTH_TOKEN:
            self.send_error(401, "Unauthorized")
            return

        if self.path == "/event":
            content_length = int(self.headers.get("Content-Length"))
            post_data = json.loads(self.rfile.read(content_length))

            # Validate data against the schema
            try:
                validate(post_data, event_schema)
            except ValidationError as e:
                self.send_error(400, "Bad Request: " + str(e))
                return
            
            event = Event.from_dict(post_data)
            self.storage.add_event(event)
            self.send_response(201)
            self.end_headers()
            return
        
        self.send_error(404, "Not Found")

    def do_GET(self):
        if self.headers.get("Authorization") != AUTH_TOKEN:
            self.send_error(401, "Unauthorized")
            return

        if self.path.startswith("/events"):
            query_string = self.path.split('?', 1)[-1]
            filters = dict(qc.split("=") for qc in query_string.split("&"))
            matching_events = self.storage.query_events(filters)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(matching_events).encode())
            return

        self.send_error(404, "Not Found")

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, AuditLogHandler)
    print("Audit Log Service running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
