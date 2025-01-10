import requests
import json

def test_mistral():
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": "Describe a fighter's combat strategy in D&D."}
        ]
    }

    try:
        response = requests.post(url, json=payload, stream=True)

        print("Response from Mistral:")
        full_content = ""
        for line in response.iter_lines():
            if line:
                # Parse the line as JSON
                try:
                    data = line.decode('utf-8')
                    json_data = json.loads(data)  # Use the `json` module here
                    if "message" in json_data and "content" in json_data["message"]:
                        full_content += json_data["message"]["content"]
                except Exception as e:
                    print(f"Error parsing line: {line} -> {e}")

        print("Final Full Response:")
        print(full_content)
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    test_mistral()
