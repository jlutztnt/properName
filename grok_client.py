import json
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GrokClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.grok.ai/v1"  # Updated API endpoint
        
    def generate_text(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7,
            "model": "grok-1"  # Added model specification
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",  # Updated to chat/completions endpoint
            headers=headers,
            json=payload,
            verify=False
        )
        
        if response.status_code != 200:
            raise Exception(f"Grok API error: {response.text}")
            
        result = response.json()
        return json.loads(result['choices'][0]['text']) 