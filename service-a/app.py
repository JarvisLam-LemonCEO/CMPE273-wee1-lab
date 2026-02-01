from flask import Flask, jsonify, request
import logging
import time
import os

# create the Flask application for Service A
app = Flask(__name__)

# Basic Logging Configuration
# Enables console logging with timestamp, level, and service name
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [ServiceA] %(message)s"
)

# Health Check Endpoint
# Used to verify whether Service A is running
# This endpoint is commonly used in distributed systems
@app.get("/health")
def health():
    return jsonify(status="ok", service="A")

# Data Endpoint (Normal Response)
# Responds to requests from other services (e.g., Service B)
# Logs each incoming request
@app.get("/data")
def data():
    logging.info("Request received: %s %s", request.method, request.path)
    # Return a simple JSON response including the process ID
    return jsonify(message="Hello from Service A", pid=os.getpid())

# Slow Endpoint (Timeout Simulation)
# Intentionally delays the response to simulate a slow provider
# Used to demonstrate request timeouts in Service B
@app.get("/slow")
def slow():
    logging.info("Request received: %s %s (slow)", request.method, request.path)
    # Artificial delay (seconds)
    time.sleep(3)
    return jsonify(message="Slow response from A")

# Application Entry Point
# Runs Service A as an independent process on port 5001
if __name__ == "__main__":
    # Port 5001 for Service A
    app.run(host="127.0.0.1", port=5001)
