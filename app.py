import os
from flask import Flask, request, jsonify
import replicate

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to the Story Generator API</h1>"

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()
    
    # Check if 'topic' is provided in the request data
    if not data or "topic" not in data:
        return jsonify({"error": "Invalid JSON or 'topic' key not provided"}), 400

    topic = data.get("topic")
    
    # Construct a prompt that asks the model to generate a story or script based on the provided topic
    prompt = f"Write a detailed story or script about: {topic}"

    response = {
        "prompt": prompt,
        "max_new_tokens": 512,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }

    try:
        # Initialize the Replicate client with the API key
        client = replicate.Client(api_token="r8_At0W8z7VBel5iRVodIXcjtViSRJML9G3TzNnL")  # Replace with actual API key
        # Use the model to generate text based on the provided topic
        output = client.run("meta/meta-llama-3-8b-instruct", input=response)
        output_text = "".join(output)  # Properly join output if it's a list of strings
        return jsonify({"story": output_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
