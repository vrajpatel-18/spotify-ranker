import requests
import json

url = 'https://api.spotify.com/v1/search'
headers = {
    'Authorization': 'Bearer BQCh0jC9S36ov6rQPPRIO2cOtWyVdekyxOHSCRR7XuqDFoPQa_GjCI2C5jPzb5eEmjG8RVlucHCqXut4PbVVbazPBeQIavOXfsyNFK8T9j62Jp_gOSo'
}

params = {
    'q': 'travis',
    'type': 'artist',
    'market': 'US',
    'limit': 10
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()

    json_data = data['artists']['items'][0]
    formatted_json = json.dumps(json_data, indent=4)
    print(formatted_json)
else:
    print(f"Request failed with status code {response.status_code}")


# import requests

# url = "https://accounts.spotify.com/api/token"
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
# }
# data = {
#     "grant_type": "client_credentials",
#     "client_id": "15eb06a1ff0a40bd95cc7c1522c5aaa3",
#     "client_secret": "32ab0e56dae8427e9efe5dab273f78a4"
# }

# response = requests.post(url, headers=headers, data=data)

# if response.status_code == 200:
#     token_data = response.json()
#     access_token = token_data.get("access_token")
#
#     print(f"Access Token: {access_token}")
# else:
#     print(f"Token request failed with status code {response.status_code}")
