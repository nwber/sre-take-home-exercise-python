import yaml
import requests
import time
import logging
from collections import defaultdict

# Logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('endpoint_health.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Function to load configuration from the YAML file
def load_config(file_path):
    logger.info('Loading config...')
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method')
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    if method is None:
        method = 'GET'

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=0.5)

        if (response.status_code < 200) | (response.status_code >= 300):
            logger.warning(f"{method} {url} response code not 2XX")
            return "DOWN"
        else:
            logger.info(f"{url} is UP!!!")
            return "UP"
    

    except requests.RequestException:
        logger.warning(f"{method} {url} failed.")
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        while_start = time.time()
        for endpoint in config:
            domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            logger.info(f"{domain} has {availability}% availability percentage")

        print("---")

        # Only sleep for 15s since the start of this loop
        while_end = time.time()
        while_delta = while_end - while_start
    
        logger.info(f"Loop duration: {while_delta}s")
        logger.info(f"Sleeping for {15 - while_delta}s")

        time.sleep(15 - while_delta)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logger.error("Usage: python monitor.py <config_file_path>")
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")