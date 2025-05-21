import requests
import time

URL = "http://127.0.0.1:5000/data"
TOTAL_REQUESTS = 20
INTERVAL = 0.2                      # Requests interval (seconds)

def stress_test():
    print(f"Sending {TOTAL_REQUESTS} requests to {URL} per {INTERVAL} seconds\n")
    for i in range(1, TOTAL_REQUESTS + 1):
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"{i:02d}: {response.json()}")
        else:
            print(f"{i:02d}: {response.status_code} - {response.json()}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    stress_test()
