import os
import requests

API_KEY = os.getenv("API_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

def query_mistral(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"prompt": prompt, "max_tokens": 150}
    response = requests.post(ENDPOINT_URL, json=payload, headers=headers)
    return response.json()
