import requests

url = 'http://127.0.0.1:5000/predict'

data = {
    "year": 2008,
    "budget": 185000000,
    "run_time_min": 152
}

response = requests.post(url, json=data)
print(response.json())