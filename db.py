from pymongo import MongoClient
import os
import json
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
password = os.environ.get("MONGO_PASSWORD")

login_string = os.environ.get("MONGO_LOGIN_STRING")
client = MongoClient(login_string)

db = client.get_database('SpotifyRanker')
users = db.users


def create_user(user_json):
    if users.count_documents({'id': user_json['id']}, limit = 1) == 0: # check that user doesn't exist
        new_user = {
            'id': user_json['id'],
            'name': user_json['display_name'],
            'img': user_json['images'][1]['url'],
            'url': user_json['external_urls']['spotify'],
            'country': user_json['country'],
            'rankings': [],
            'friends': []
        }
        users.insert_one(new_user)
        print("User created")
    else:
        print("User already exists")
    
    
# {
#     "display_name": "vraj patel",
#     "external_urls": {
#         "spotify": "https://open.spotify.com/user/vrajiepoo"
#     },
#     "href": "https://api.spotify.com/v1/users/vrajiepoo",
#     "id": "vrajiepoo",
#     "images": [
#         {
#             "url": "https://i.scdn.co/image/ab67757000003b82805c6cd2fa013a9ade12127d",
#             "height": 64,
#             "width": 64
#         },
#         {
#             "url": "https://i.scdn.co/image/ab6775700000ee85805c6cd2fa013a9ade12127d",
#             "height": 300,
#             "width": 300
#         }
#     ],
#     "type": "user",
#     "uri": "spotify:user:vrajiepoo",
#     "followers": {
#         "href": null,
#         "total": 14
#     },
#     "country": "US",
#     "product": "premium",
#     "explicit_content": {
#         "filter_enabled": false,
#         "filter_locked": false
#     }
# }