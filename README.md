# Dynamic Rate Limiter (Token Bucket) – Flask API

This is a simple implementation of a **Token Bucket Rate Limiter** using Python and Flask. It limits the number of incoming requests **per client IP** and supports **dynamic reconfiguration** of the rate limit via an API.

## Features

- Token Bucket algorithm
- Per-client rate limiting based on IP
- Configurable `capacity` and `refill_rate` via `POST /config`
- Thread-safe implementation using locks
- Simple stress test script to simulate traffic

---

## Requirements

```bash
pip install -r requirements.txt
```
## How to Run
Start the server:
```bash
python app.py
```

The server will run at:
http://127.0.0.1:5000

## Stress Test
Simulate incoming requests:
```bash
python stress_test.py
```
You can change the following values in stress_test.py to adjust load:
- TOTAL_REQUESTS
- INTERVAL

## Dynamic Configuration
Change the rate limit in real-time by sending a POST request to /config.
Example using curl:
```bash
curl -X POST http://127.0.0.1:5000/config -H "Content-Type: application/json" -d '{"capacity": 15, "refill_rate": 5}'
```
This updates:
- capacity: max number of tokens
- refill_rate: how many tokens are added per second. After this change, all token buckets are reset with the new configuration changed dynamically.

## Explanation
- Each IP gets its own TokenBucket.
- A token is consumed per request.
- If no tokens are available, the server returns HTTP 429 – Too Many Requests.
- Tokens are refilled gradually over time (refill_rate tokens per second), up to capacity.

## Example Output (Stress Test)

```bash
01: {'from': '127.0.0.1', 'message': 'Access granted'}
02: {'from': '127.0.0.1', 'message': 'Access granted'}
03: {'from': '127.0.0.1', 'message': 'Access granted'}
04: {'from': '127.0.0.1', 'message': 'Access granted'}
05: {'from': '127.0.0.1', 'message': 'Access granted'}
06: {'from': '127.0.0.1', 'message': 'Access granted'}
07: {'from': '127.0.0.1', 'message': 'Access granted'}
08: {'from': '127.0.0.1', 'message': 'Access granted'}
09: {'from': '127.0.0.1', 'message': 'Access granted'}
10: {'from': '127.0.0.1', 'message': 'Access granted'}
11: {'from': '127.0.0.1', 'message': 'Access granted'}
12: {'from': '127.0.0.1', 'message': 'Access granted'}
13: 429 - {'error': 'Too Many Requests'}
14: 429 - {'error': 'Too Many Requests'}
15: 429 - {'error': 'Too Many Requests'}
16: {'from': '127.0.0.1', 'message': 'Access granted'}
17: 429 - {'error': 'Too Many Requests'}
18: 429 - {'error': 'Too Many Requests'}
19: 429 - {'error': 'Too Many Requests'}
20: 429 - {'error': 'Too Many Requests'}
```
