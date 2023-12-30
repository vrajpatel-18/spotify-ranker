from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
password = os.environ.get("MONGO_PASSWORD")

login_string = os.environ.get("MONGO_LOGIN_STRING")
client = MongoClient(login_string)

db = client.get_database('SpotifyRanker')
users = db.users

new_user = {
    'id': 'vrajiepoo',
    'name': 'vraj patel',
    'img': 'https://i.scdn.co/image/ab6775700000ee85805c6cd2fa013a9ade12127d',
    'url': 'https://open.spotify.com/user/vrajiepoo',
    'country': 'US',
    'rankings': [
        {
            'type': 'album',
            'id': '41GuZcammIkupMPKH2OJ6I',
        }
    ],
    'friends': [
        
    ]
}

# users.insert_one(new_user)
print(pprint(list(users.find({}))))