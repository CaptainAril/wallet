import json
import logging
import time

import requests
from django.conf import settings
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

class ServiceUnavailableError(Exception):
    pass


class ServiceProxy:
    def __init__(self, service_name):
        self.service_config = settings.MICROSERVICES.get(service_name)
        if not self.service_config:
            raise ValueError(f"Service '{service_name}' not configured")
        
        self.base_url = self.service_config.get("url")
        self.timeout = self.service_config.get("timeout", 30)
        self.retries = self.service_config.get("retries", 3)

    
    def forward_request(self, request_path, method, headers=None, body=None, params=None):
        url = f"{self.base_url}/{request_path.lstrip('/')}"
        headers = headers or {}

        # if 'host' in headers:
        #     del headers['host']

        attempt = 0
        start_time = time.time()

        while attempt < self.retries:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    data=body,
                    params=params,
                    timeout=self.timeout,
                )

                elapsed_time = time.time() - start_time
                logger.info(f"Request to {url} completed in {elapsed_time:.2f}s with status code {response.status_code}")

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "content": response.json() if response.headers.get("Content-Type") == "application/json" else response.content,
                }

            except RequestException as e:
                attempt += 1
                logger.warning(f"Request to {url} failed (attempt {attempt}): {str(e)}")

                if attempt >= self.retries:
                    raise ServiceUnavailableError(f"Service {self.base_url} is unavailable")
                time.sleep(0.5 * attempt)
