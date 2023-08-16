import unittest
from http.server import HTTPServer
from threading import Thread
from main import AuditLogHandler
import requests
import random
import uuid

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

    def generate_random_event():
        event_types = ["account_created", "action_performed", "account_billed", "account_deactivated"]
        user_ids = [str(uuid.uuid4()) for _ in range(5)] # Generating 5 unique user IDs

        return {
            "event_type": random.choice(event_types),
            "user_id": random.choice(user_ids),
            "variant_data": {"response": "this is a randomized event"} # You can randomize this field as well if needed
        }

    def test_post_event(self):
        url = 'http://localhost:8000/event'
        headers = {'Authorization': 'secret_token', 'Content-Type': 'application/json'}
        data = AuditLogServiceTest.generate_random_event()
        response = requests.post(url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_query_events(self):
        url = 'http://localhost:8000/events?event_type=account_created'
        headers = {'Authorization': 'secret_token', 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on expected response

if __name__ == '__main__':
    unittest.main()
