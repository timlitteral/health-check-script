import yaml
import requests
import time
import argparse
from collections import defaultdict
from datetime import datetime

class Endpoint:
    def __init__(self, name, url, method="GET", headers=None, body=None):
        if headers is None:
            headers = {}
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

def check_endpoint(endpoint):
    try:
        response = requests.request(
            method=endpoint.method,
            url=endpoint.url,
            headers=endpoint.headers,
            data=endpoint.body,
            timeout=5  # Add a timeout for requests
        )
        response_time = response.elapsed.total_seconds() * 1000  # Convert to milliseconds
        response_code = response.status_code
        status = ""

        if response_code >= 200 and response_code < 300 and response_time < 500:
            status = f"UP"
        elif response_code >= 200 and response_code < 300 and response_time >= 500:
            # Response latency exceeds 500ms
            status = (f"DOWN (response latency is not less than 500 ms)")
        elif response_code == 400:
            status = f"DOWN (HTTP 400 Bad Request)"
        elif response_code == 403:
            # Explicitly handling HTTP 403 Forbidden
            status = f"DOWN (HTTP 403 Forbidden)"
        elif response_code == 404:
            status = f"DOWN (HTTP 404 Not Found)"
        elif response_code == 500:
            status = f"DOWN (HTTP 500 Internal Server Error)"
        else:
            status = f"DOWN (HTTP {response_code})"

        return response_code, int(response_time), status

    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        print(f"Error checking {endpoint.name}: {e}")
        return None, None, "DOWN (Error)"


def main():
    parser = argparse.ArgumentParser(description="Health Check for HTTP Endpoints")
    parser.add_argument("config_file", help="Path to the YAML configuration file")
    args = parser.parse_args()

    with open(args.config_file, 'r') as f:
        endpoints_data = yaml.safe_load(f)

    endpoints = []
    for endpoint_data in endpoints_data:
        name = endpoint_data.get('name')
        url = endpoint_data.get('url')
        method = endpoint_data.get('method', "GET")
        headers = endpoint_data.get('headers', {})
        body = endpoint_data.get('body')
        endpoints.append(Endpoint(name, url, method, headers, body))

    domain_availability = defaultdict(int)  # Tracks total requests per domain
    endpoint_results = defaultdict(list)  # Stores results for each endpoint
    log_file = "health_check_log.txt"

    start_time = time.time()  # Track the actual start time for the first cycle
    cycle_number = 1

    while True:
        current_time = time.time() - start_time  # Time elapsed since start
        sleep_time = (15 * cycle_number) - current_time  # Calculate how long to wait before next cycle
        
        if sleep_time > 0:
            time.sleep(sleep_time)  # Wait until the next 15-second interval
        
        log_message = f"\n{datetime.now()}\n"  # Add blank line and timestamp
        log_message += f"Test cycle #{cycle_number} begins at time = {int(current_time)} seconds:\n"

        for endpoint in endpoints:
            # Safely extract the domain from the URL
            try:
                domain = endpoint.url.split('/')[2]  # Extract domain name
            except IndexError:
                domain = "Unknown"

            domain_availability[domain] += 1
            response_code, response_time, status = check_endpoint(endpoint)
            
            if response_code is not None:
                # Check if the response is DOWN due to high latency and format accordingly
                if "response latency" in status:
                    log_message += (f"Endpoint with name {endpoint.name} has HTTP response code {response_code} and\n"
                                    f"response latency {response_time} ms => {status}\n")
                else:
                    log_message += (f"Endpoint with name {endpoint.name} has HTTP response code {response_code} and "
                                    f"response latency {response_time} ms => {status}\n")
            else:
                log_message += (f"Endpoint with name {endpoint.name} could not be reached => {status}\n")

            endpoint_results[endpoint.url].append(status)

        for domain, total_requests in domain_availability.items():
            # Count the number of UP statuses for each domain
            up_count = sum(
                1 for url in endpoint_results if url.split('/')[2] == domain and
                all(isinstance(status, str) and not status.startswith("DOWN") for status in endpoint_results[url])
            )
            availability_percentage = round((up_count / total_requests) * 100)
            log_message += f"{domain} has {availability_percentage}% availability percentage\n"
            print(f"{domain} has {availability_percentage}% availability percentage")

        with open(log_file, "a", encoding="utf-8") as f:  # Use utf-8 encoding
            f.write(log_message)

        domain_availability.clear()  # Reset for next cycle
        endpoint_results.clear()
        cycle_number += 1

if __name__ == "__main__":
    main()