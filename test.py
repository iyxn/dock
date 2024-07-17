import requests

url = "http://localhost:8001/generate"

data = {
    "messages": "apa itu bahasa python",
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 200
    }
}

response = requests.post(url, json=data)

if response.status_code == 200:
    try:
        print(response.json())

        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        print(text)

    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Error: {response.status_code}, Detail: {response.text}")

#curl -X POST "http://127.0.0.1:8001/generate" \
#-H "Content-Type: application/json" \
#-d '{"messages": "apa itu bahasa python", "generationConfig": { "temperature": 0.7, "maxOutputTokens": 200 }}'
