import concurrent.futures
import json
import os
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

URL = "http://localhost:5001/login"
TOTAL_REQUESTS = 400
WORKERS = 5

username = os.environ.get("LOAD_TEST_USERNAME")
password = os.environ.get("LOAD_TEST_PASSWORD")

if not username or not password:
    raise SystemExit(
        "Set LOAD_TEST_USERNAME and LOAD_TEST_PASSWORD before running."
    )


def send_login(_):
    payload = json.dumps({
        "username": username,
        "password": password
    }).encode("utf-8")

    request = urllib.request.Request(
        URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    start = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            status = response.status
            response.read()
    except urllib.error.HTTPError as error:
        status = error.code
        error.read()
    except Exception as error:
        # Log the error type only, never request data or credentials.
        status = f"CONNECTION_ERROR:{type(error).__name__}"

    elapsed = time.perf_counter() - start
    return status, elapsed


print(f"Starting login load test: {TOTAL_REQUESTS} requests, "
      f"{WORKERS} workers")

start = time.perf_counter()

with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(send_login, range(TOTAL_REQUESTS)))

duration = time.perf_counter() - start
statuses = Counter(status for status, _ in results)
latencies = [elapsed * 1000 for _, elapsed in results]

successful = statuses.get(200, 0)
failed = TOTAL_REQUESTS - successful

print("\n--- Load Test Results ---")
print(f"Total requests: {TOTAL_REQUESTS}")
print(f"Duration: {duration:.2f} seconds")
print(f"Throughput: {TOTAL_REQUESTS / duration:.2f} requests/second")
print(f"Successful logins: {successful}")
print(f"Failed requests: {failed}")
print(f"HTTP/status breakdown: {dict(statuses)}")
print(f"Average response time: {statistics.mean(latencies):.2f} ms")
print(f"Median response time: {statistics.median(latencies):.2f} ms")
print(f"P95 response time: "
      f"{sorted(latencies)[int(0.95 * (len(latencies) - 1))]:.2f} ms")
