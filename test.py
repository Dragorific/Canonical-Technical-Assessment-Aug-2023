import unittest
from http.server import HTTPServer
from threading import Thread
from main import AuditLogHandler
import requests

class AuditLogServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.server_address = ('', 8000)
        cls.server = HTTPServer(cls.server_address, AuditLogHandler)
        cls.thread = Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        # Stop the server
        cls.server.shutdown()
        cls.thread.join()

    def test_post_event(self):
        url = 'http://localhost:8000/event'
        headers = {'Authorization': 'secret_token', 'Content-Type': 'application/json'}
        data = {"event_type": "account_created", "user_id": "123", "variant_data": {}}
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
