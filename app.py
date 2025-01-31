from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from grok_client import GrokClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Debug: Print all environment variables
logger.info("Environment variables:")
for key, value in os.environ.items():
    logger.info(f"{key}: {'*' * len(value)}")  # Mask the values for security

app = Flask(__name__)

# Move API key check into the analyze_name route
grok_client = None

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze-name', methods=['POST'])
def analyze_name():
    global grok_client
    
    # Initialize grok_client if not already done
    if grok_client is None:
        api_key = os.getenv('GROK_API_KEY')
        if not api_key:
            logger.error("GROK_API_KEY environment variable is not set")
            return jsonify({
                'error': 'API key not configured'
            }), 500
        try:
            grok_client = GrokClient(api_key=api_key)
            logger.info("GrokClient initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GrokClient: {str(e)}")
            return jsonify({
                'error': f'Failed to initialize API client: {str(e)}'
            }), 500
    
    data = request.get_json()
    
    if not data or 'first_name' not in data or 'last_name' not in data:
        return jsonify({
            'error': 'Missing required fields: first_name and last_name'
        }), 400
    
    first_name = data['first_name'].strip()
    last_name = data['last_name'].strip()
    
    # Analyze name using Grok
    prompt = f"""
    Analyze if '{first_name} {last_name}' is a proper name. Consider:
    1. Is it properly capitalized?
    2. Does it contain any numbers or special characters?
    3. Does it follow common name patterns?
    
    Return a JSON with:
    - is_valid: boolean
    - formatted_name: properly formatted version
    - reasons: list of any issues found
    """
    
    try:
        response = grok_client.generate_text(prompt)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000))) 