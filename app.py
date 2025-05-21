from flask import Flask, request, jsonify
from limiter import TokenBucket
from config import config

app = Flask(__name__)

# Buckets IP
buckets = {}

def get_bucket(client_id):
    if client_id not in buckets:
        buckets[client_id] = TokenBucket(
            capacity=config["capacity"],
            refill_rate=config["refill_rate"]
        )
    return buckets[client_id]

# Decorator
def rate_limited(f):
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr
        bucket = get_bucket(client_ip)
        if bucket.consume():
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Too Many Requests"}), 429
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/data")
@rate_limited
def protected_data():
    return jsonify({"message": "Access granted", "from": request.remote_addr})

# Endpoint for modifying the rate limit
@app.route("/config", methods=["POST"])
def update_config():
    data = request.get_json()
    if "capacity" in data:
        config["capacity"] = data["capacity"]
    if "refill_rate" in data:
        config["refill_rate"] = data["refill_rate"]
    # Restart buckets
    for ip in buckets:
        buckets[ip] = TokenBucket(config["capacity"], config["refill_rate"])
    return jsonify({"message": "Config updated", "new_config": config})

if __name__ == "__main__":
    app.run(debug=True)
