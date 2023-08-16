from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonschema import validate, ValidationError
from prometheus_client import start_http_server
from multiprocessing import Process
from Event import *
from EventStorage import *
from schemas import event_schema
from metrics import *
from database import *
from app import start_flask_app

AUTH_TOKEN = "secret_token"  # Simple authentication token

class AuditLogHandler(BaseHTTPRequestHandler):
    storage = EventStorage()

    def handle_request(self, method):
        endpoint = self.path.split('?')[0]
        with RESPONSE_TIME.labels(method=method, endpoint=endpoint).time():
            if method == 'POST':
                self.process_POST()
            elif method == 'GET':
                self.process_GET()
            REQUESTS.labels(method=method, endpoint=endpoint).inc()

    def process_POST(self): 
        if self.headers.get("Authorization") != AUTH_TOKEN:
            self.send_error(401, "Unauthorized")
            return

        if self.path == "/event":
            content_length = int(self.headers.get("Content-Length"))
            post_data = json.loads(self.rfile.read(content_length))

            # Validate data against the schema
            try:
                validate(post_data, event_schema)
                print(f"Successfully validated data from: {self.client_address}")
                print(f"Data: {post_data}")
            except ValidationError as e:
                self.send_error(400, "Bad Request: " + str(e))
                return
            
            event = Event.from_dict(post_data)
            add_event(event)
            self.storage.add_event(event)
            self.send_response(201)
            self.end_headers()
            return
        
        self.send_error(404, "Not Found")

    def process_GET(self):
        if self.headers.get("Authorization") != AUTH_TOKEN:
            self.send_error(401, "Unauthorized")
            return

        if self.path.startswith("/events"):
            query_string = self.path.split('?', 1)[-1]
            filters = dict(qc.split("=") for qc in query_string.split("&"))
            matching_events = query_events(filters)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(matching_events).encode())
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        self.handle_request('POST')

    def do_GET(self):
        self.handle_request('GET')

def run_server():
    # Create the SQLite3 database
    create_database()

    # Start the Augit Log HTTP server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, AuditLogHandler)
    print("Audit Log Service running on port 8000...")

    # Start Flask app as a daemon
    flask_process = Process(target=start_flask_app)
    flask_process.daemon = True
    flask_process.start()
    
    # Start the Prometheus metrics server
    start_http_server(8001)
    print("Metrics available at http://localhost:8001/metrics")
    
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
