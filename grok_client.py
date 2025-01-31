import json
import requests
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class GrokClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.x.ai"  # Updated base URL
        
    def generate_text(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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