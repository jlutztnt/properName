import json
import requests

class GrokClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.xai.sh/v1"  # Grok API endpoint
        
    def generate_text(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"Grok API error: {response.text}")
            
        result = response.json()
        return json.loads(result['choices'][0]['text']) 