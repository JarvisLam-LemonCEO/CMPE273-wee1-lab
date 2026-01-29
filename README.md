# CMPE 273 Week 1 Lab
## Author of this project: Hei Lam (014751503)

## Objective
The goal of this lab is to experience the core characteristics of a distributed system by building a small but real system locally.

This lab demonstrates:

- Independent services running as separate processes
- Communication over a network
- Failure propagation across service boundaries
- Basic logging and graceful error handling

Although both services run on the same machine, they behave as independent distributed components.


## System Overview

This system consists of two services:

### Service A (Provider)
- Runs independently on its own port
- Exposes a simple HTTP API
- Responds to requests from other services
- Logs incoming requests

### Service B (Consumer)
- Runs independently on its own port
- Exposes its own HTTP API
- Calls Service A over the network
- Handles failures gracefully when Service A is unavailable or slow

### Each Service:
- Runs as a separate process
- Listens on a different port
- Communicates via HTTP network calls


## How to run the Lab
### Step 1: Start Service A (Provider)

Open **Terminal 1**:
```bash
cd week1-lab/service-a
Python -m venv venv
source venv/bin/activate (macOS)
.\venv/Scripts\activate (Windows)
pip install flask requests
python app.py
```
Service A run on: http://127.0.0.1:5001
Test Service A: curl http://127.0.0.1:5001/data

### Step 2: Start Service B (Consumer)
Open **Terminal 2 (must be separate from Service A)**
```bash
cd week1-lab/service-b
python -m venv venv
source venv/bin/activate (macOS)
.\venv/Scripts\activate (Windows)
pip install flask requests
python app.py
```

Service B runs on: http://127.0.0.1:5002

Test Service B: curl http://127.0.0.1:5002/combine

## Demonstrating Distributed System Behavior
### Case 1: Normal Operation
with both services running:
```curl - i http://127.0.0.1:5002/combine
```

Expected behavior:
- Service B successfully calls Service A
- Response includes data from both services
- Logs appear in both terminal windows

### Case 2: Service A Failure
Stop Service A using Ctrl + C.
Call Service B again:

```curl -i http://127.0.0.1:5002/combine
```
Expected behavior:
- Service B returns HTTP 503
- Response indicates Service A is unavailable
- Service B continues running normally
- Failure is isolated and handled gracefully

### Case 3: Timeout / Slow Dependency
Restart Service A.
Modify Service B to call the slow endpoint:
```requests.get("http://127.0.0.1:5001/slow", timeout=1.0)
```
Call Service B again:
```curl -i http://127.0.0.1:5002/combine

```
Expected behavior:
- Service B returns HTTP 504
- Timeout error is logged
- Service B remains responsive