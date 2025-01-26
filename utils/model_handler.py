import os
import requests

API_KEY = os.getenv("API_KEY")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

# Function to query MaaS Mistral model
def query_mistral(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "mistral-7b-instruct",
        "prompt": prompt,
        "max_tokens": 100,
    }
    response = requests.post(f"{ENDPOINT_URL}/v1/completions", json=payload, headers=headers)
    
    # Log raw response for debugging
    print("Raw Response:", response.text)
    
    # Check for HTTP errors
    response.raise_for_status()
    
    # Parse and return JSON
    try:
        return response.json()
    except ValueError:
        print("Invalid JSON response:", response.text)
        return {"error": "Invalid JSON"}
