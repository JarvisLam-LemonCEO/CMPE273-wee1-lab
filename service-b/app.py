from flask import Flask, jsonify, request
import logging
import os
import requests

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [ServiceB] %(message)s"
)

SERVICE_A_URL = "http://127.0.0.1:5001"

@app.get("/health")
def health():
    return jsonify(status="ok", service="B")

@app.get("/combine")
def combine():
    logging.info("Request received: %s %s", request.method, request.path)

    try:
        # Handles failures gracefully when service A is unavailable
        # 503
        # r = requests.get(f"{SERVICE_A_URL}/data", timeout=1.0) 
        # 504 time out
        r = requests.get(f"{SERVICE_A_URL}/slow", timeout=1.0)
        r.raise_for_status()
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="reachable",
            from_a=r.json()
        ), 200

    except requests.exceptions.ConnectionError:
        logging.warning("Service A unavailable (connection error)")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="unavailable",
            from_a=None
        ), 503

    except requests.exceptions.Timeout:
        logging.warning("Service A timed out")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="timeout",
            from_a=None
        ), 504

    except Exception as e:
        logging.exception("Unexpected error in /combine")
        return jsonify(
            from_b="Hello from Service B",
            pid=os.getpid(),
            a_status="error",
            error=str(e),
            from_a=None
        ), 502


if __name__ == "__main__":
    # Port 5002 for Service B
    app.run(host="127.0.0.1", port=5002, debug=False, use_reloader=False)
