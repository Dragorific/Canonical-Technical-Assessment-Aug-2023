from prometheus_client import Counter, Histogram

REQUESTS = Counter('requests_total', 'Total number of requests', ['method', 'endpoint'])
ERRORS = Counter('errors_total', 'Total number of errors', ['method', 'endpoint', 'status'])
RESPONSE_TIME = Histogram('response_time_seconds', 'Histogram of response time for method', ['method', 'endpoint'])