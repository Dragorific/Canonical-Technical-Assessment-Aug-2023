# Canonical-Technical-Assessment-Aug-2023
 
**Deployment Instructions for Ubuntu**
_Prerequisites_
- Python 3.x
- Virtual environment (optional but recommended)

_Steps_
1. Clone the Repository: Clone the Git repository containing your project files.
2. Navigate to the Project Directory: Navigate to the directory containing the project files using the terminal.
3. Create a Virtual Environment (Optional): Create a virtual environment to isolate dependencies.

python3 -m venv env
source env/bin/activate

4. Install Required Dependencies: Use the requirements.txt file.

pip install -r requirements.txt

5. Run the Application: Start the Flask application using the command:

python app.py

**Testing Instructions Using cURL**

Testing Using cURL
cURL is a command-line tool that allows you to make HTTP requests. Assuming you have endpoints for adding and retrieving events, here's how you can test them:

Retrieve All Events:
curl http://localhost:5000/  # Replace with the correct endpoint if needed

Add a New Event (modify the URL and JSON data as needed):
curl -X POST -H "Content-Type: application/json" -d '{"timestamp": "2023-08-11", "event_type": "account_created", "user_id": "1234", "variant_data": "data_here"}' http://localhost:5000/add_event

Testing Using Postman
Postman is a popular tool for testing APIs that provides a graphical user interface. Here's how you can test the audit log service using Postman:

Retrieve All Events:

Method: GET
URL: http://localhost:5000/ (or the correct endpoint)
Click "Send"
Add a New Event:

Method: POST
URL: http://localhost:5000/add_event (or the correct endpoint)
Headers: Key = Content-Type, Value = application/json
Body: Choose "raw" and "JSON", and enter the following JSON data:
{
  "timestamp": "2023-08-11",
  "event_type": "account_created",
  "user_id": "1234",
  "variant_data": "data_here"
}
Click "Send"

**Design and Architecture Decisions**
_Database_
SQLite: A lightweight database used for simplicity and ease of setup. It's suitable for small to medium-sized applications.
Trade-offs: While convenient, SQLite may not be suitable for very large datasets or high-concurrency workloads.
_Web Framework_
Flask: A minimal and flexible web framework used to build the web interface and API.
Rationale: Flask allows rapid development and easy integration with the existing codebase without unnecessary complexity.
_Data Model_
Flexible Schema: The schema is designed to handle various event types without modification.
Rationale: This approach supports an open-ended list of event types, making the system more extensible.
_Security_
Note: Authentication was mentioned but not implemented in the code snippets. In a production environment, proper authentication and authorization should be implemented.

**Conclusion**
This document provides a comprehensive guide to deploying, testing, and understanding the audit log service. The system is designed with flexibility and simplicity in mind, but there are areas for further improvement and scaling as mentioned in the additional notes.
