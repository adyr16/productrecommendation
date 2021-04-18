import requests
data = {
    "user_id": "abc"
  }

url = "http://127.0.0.1:5000/recommendations"
response = requests.post(url, json=data)
print("Top 5 Recommendations: "+ str(response.json()))