import requests

response = requests.post("http://127.0.0.1:50100/predict", json={"input": 4.0})
print(f"Status: {response.status_code}\nResponse:\n {response.text}")