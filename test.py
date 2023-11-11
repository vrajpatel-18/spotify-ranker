import requests
import json
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


searchTerm = "d"
searchLimit = '20'


searchType = "artist"
url = 'https://api.spotify.com/v1/search?q=' + searchTerm + '&type=' + searchType + '&limit=' + searchLimit
headers = {
    'Authorization': 'Bearer BQBsL9ThtgScnGansttCP69eXffmWd7N7g1n5LA9uTztriL2JGnl7H9rbB3AI1nQHoTX4QNND62czMsgUuOHwHAy3wsNzKx9f67D9l5wXlz5TH5qPfU'
}
artist_response = requests.get(url, headers=headers)

searchType = "album"
url = 'https://api.spotify.com/v1/search?q=' + searchTerm + '&type=' + searchType + '&limit=' + searchLimit
headers = {
    'Authorization': 'Bearer BQBsL9ThtgScnGansttCP69eXffmWd7N7g1n5LA9uTztriL2JGnl7H9rbB3AI1nQHoTX4QNND62czMsgUuOHwHAy3wsNzKx9f67D9l5wXlz5TH5qPfU'
}
album_response = requests.get(url, headers=headers)


artist_data = artist_response.json()
album_data = album_response.json()

artists = []
artistsPop = []
for artist in artist_data['artists']['items']:
    artists.append(artist['name'])
    artistsPop.append(artist['followers']['total'])
    
for i in range(len(artists)):
    # print(artist + ": " + str(similar(searchTerm, artist)))
    print(artists[i], '{:,}'.format(artistsPop[i]))
    

# albums = []
# for album in album_data['albums']['items']:
#     albums.append(album['name'])
    
# for album in albums:
#     print(album + ": " + str(similar(searchTerm, album)))

# json_data = artist_data
# formatted_json = json.dumps(json_data, indent=4)
# print(formatted_json)




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

#     print(f"Access Token: {access_token}")
# else:
#     print(f"Token request failed with status code {response.status_code}")