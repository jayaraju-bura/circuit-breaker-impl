import http

import requests

import functools

from circuit_breaker import circuit_breaker

faulty_endpoint = "http://127.0.0.1:5000/negative"
success_endpoint = "http://127.0.0.1:5000/positive"
random_status_endpoint = "http://127.0.0.1:5000/arbitrary"


@circuit_breaker()
def make_request(url):
    try:
        response = requests.get(url, timeout=0.3)
        print("inside make_request")
        if response.status_code == http.HTTPStatus.OK:
            print(f"Call to {url} succeed with status code = {response.status_code}")
            return response
        if 500 <= response.status_code < 600:
            print(f"Call to {url} failed with status code = {response.status_code}")
            raise Exception("Server Issue")
    except Exception:
        print(f"Call to {url} failed")
        raise
