import requests
import json

url = "http://192.168.1.7:5000/sh-wsmp"
params = {
    'mantra_index': '1.1.1',
    'mantra': 'अ॒ग्निना॑ र॒यिम॑श्नव॒त्पोष॑मे॒व दि॒वेदि॑वे । य॒शसं॑ वी॒रव॑त्तमम् ॥'
}

response = requests.get(url, params=params)

try:
    data = json.dumps(response.json(), ensure_ascii=False)
    print(data)
except ValueError as e:
    print(f"Failed to parse JSON: {e}")
    print(f"Response content: {response.text}")
