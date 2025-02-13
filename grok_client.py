import json
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GrokClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = "https://api.x.ai"  # Updated base URL
        
    def generate_text(self, prompt):
        if not self.api_key:
            raise ValueError("API key is not set")
            
        # Remove 'Bearer ' if it's already in the API key
        token = self.api_key.replace('Bearer ', '')
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that analyzes names. You respond in JSON format with is_valid (boolean), formatted_name (string), and reasons (array of strings)."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "grok-2-latest"
        }
        
        response = requests.post(
            f"{self.base_url}/v1/chat/completions",
            headers=headers,
            json=payload,
            verify=False
        )
        
        if response.status_code != 200:
            raise Exception(f"Grok API error: {response.text}")
            
        result = response.json()
        return json.loads(result['choices'][0]['message']['content']) 