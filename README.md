# Canonical-Technical-Assessment-Aug-2023
## Deployment Instructions for Ubuntu
### _Prerequisites_
- Python 3.x
- Virtual environment (optional but recommended)
### List of the Frameworks and Libraries used:
- **Flask:** A micro web framework used to build the web interface for visualizing the audit log events.
- **SQLite:** A C library that provides a lightweight, disk-based database used for storing the audit log events.
- **HTTP.server:** A module in Python's standard library used to build the custom HTTP server (AuditLogHandler) for handling the audit log events.

### _Steps_
1. Clone the Repository: Clone the Git repository containing your project files.
2. Navigate to the Project Directory: Navigate to the directory containing the project files using the terminal.
3. Ensure Python and pip are updated
```
sudo apt update
sudo apt install python3 python3-pip
```
4. Create a Virtual Environment (Optional): Create a virtual environment to isolate dependencies.
```
sudo apt install python3-venv  # Install the venv module if not already installed
python3 -m venv myenv          # Create a new virtual environment named 'myenv'
source myenv/bin/activate      # Activate the virtual environment
```
5. Install Required Dependencies: Use the requirements.txt file.
```
pip3 install -r requirements.txt
```
6. Run the AuditLog service: Start the HTTP application using the command:
```
python3 main.py
```
7. Run the unit tests by using the command:
```
python3 test.py
```
## Testing Instructions

### AuditLogHandler (HTTP Server on Port 8000)
**Testing Using cURL**\
Add a New Event:
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: secret_token" -d '{"event_type": "account_created", "user_id": "1234", "variant_data": {"response": "data_here"}}' http://localhost:8000/event
```
Query Events (modify the URL and query parameters as needed):
```
curl -H "Authorization: secret_token" http://localhost:8000/events?event_type=account_created
```
\
**Testing Using Postman**\
Add a New Event:
```
Method: POST
URL: http://localhost:8000/event
Headers: 
- Key = Content-Type, Value = application/json
- Key = Authorization, Value = secret_token
Body: Enter the event JSON data.
```
Click "Send"

Query Events:
```Method: GET
URL: http://localhost:8000/events (add query parameters as needed)
Headers: 
- Key = Content-Type, Value = application/json
- Key = Authorization, Value = secret_token
```
Click "Send"

### Flask App (Port 5000)
Run app.py and open: http://localhost:5000/ \
This web interface allows you to view the various requests coming in and out

### Prometheus Metrics (Port 8001)
**Accessing Prometheus Metrics:**\
You can also check the Prometheus metrics by making a GET request to the /metrics endpoint on port 8001:
```
curl http://localhost:8001/metrics
```
This will provide you with a list of metrics and their current values.

## Design and Architecture Decisions
- **Database:** SQLite, a lightweight database used for simplicity and ease of setup. It's suitable for small to medium-sized applications.
- Trade-offs: While convenient, SQLite may not be suitable for very large datasets or high-concurrency workloads.
- **Web Framework:** Flask, a minimal and flexible web framework used to build the web interface and API.
- Rationale: Flask allows rapid development and easy integration with the existing codebase without unnecessary complexity.
- **Data Model:** Flexible Schema, the schema is designed to handle various event types without modification.
- Rationale: This approach supports an open-ended list of event types, making the system more extensible.
- **Security:** A basic authentication token is used to validate whether the API service can be used or not, depending on if the user is aware of the API token.

## Future Considerations
### Encryption:
**Why?**\
Given that audit logs can contain sensitive information about user activities, it's crucial to ensure this data is protected both in transit and at rest.

**Advantages:**
- Data Security: Encryption ensures that your data is unreadable to unauthorized users, even if they gain access to it.
- Compliance: Many regulations (like GDPR, HIPAA, etc.) mandate the encryption of sensitive data.
- Trust: Users and stakeholders have more trust in a system that takes data security seriously.

**Drawbacks:**
- Performance Overhead: Encrypting and decrypting data requires computational resources. This might introduce latency, especially if the volume of data is large.
- Complexity: Implementing encryption, key management, and ensuring that only authorized services can decrypt the data introduces complexity.
- Key Management: Managing and rotating encryption keys is crucial. If a key is lost, the encrypted data might become irrecoverable. If a key is compromised, the data is at risk.
### Using a Queuing Protocol (e.g., RabbitMQ):
**Why?**\
As your service scales and becomes write-intensive, direct writes to the database can become a bottleneck. A queuing protocol can decouple data ingestion from data storage, providing a buffer.

**Advantages:**
- Scalability: A queuing system can absorb high spikes in incoming data, ensuring the system remains responsive even under heavy load.
- Reliability: If your database or storage system becomes temporarily unavailable, the queuing system can hold onto the data until it's back online.
- Decoupling: Separates the concerns of data ingestion and data processing/storage. This makes the system more modular and easier to maintain.
- Order Preservation: Some queuing systems can ensure that messages are processed in the order they're received, which can be crucial for certain applications.

**Drawbacks:**
- Complexity: Introducing a queuing system adds another component to manage and monitor.
- Latency: While queuing systems can handle large volumes of data, they might introduce a slight delay from when data is received to when it's processed.
- Data Durability: If the queuing system isn't set up with durability in mind (e.g., persistent queues), there's a risk of data loss if the queue goes down.

## Conclusion
This document provides a comprehensive guide to deploying, testing, and understanding the audit log service. The system is designed with flexibility and simplicity in mind, but there are areas for further improvement and scaling as mentioned in the additional notes.
