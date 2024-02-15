from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
password = os.environ.get("MONGO_PASSWORD")

login_string = os.environ.get("MONGO_LOGIN")
client = MongoClient(login_string)

db = client.get_database('SpotifyRanker')
users = db.users
albums = db.albums
artists = db.artists
playlists = db.playlists

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

new_album_ranking = {
    'id': '0On7uutIu9rZRvP9aJbMog',
    'unranked': [],
    'ranked': [
        "2HALQBSAvpw1oCzL5QsrT2",
        "08YvUaUsZktAG6zEMDwUqO",
        "00ZQQArUJReFfsMnl8dIgd",
        "2VjOTvl50tscmc0RDjPdr2"
    ],
    'type': 'artist',
    'user_id': 'vrajiepoo'
}

# add album to user's rankings array
users.update_one({'id': 'vrajiepoo'}, {"$pull": {"rankings": {"id": new_album_ranking["id"]}}})
users.update_one({'id': 'vrajiepoo'}, {'$push': {'rankings': new_album_ranking}})

# add album to albums collection
filter_criteria = {
    "id": new_album_ranking['id'],
    "user_id": new_album_ranking['user_id']
}
if new_album_ranking['type'] == 'album':
    result = albums.replace_one(filter_criteria, new_album_ranking, upsert=True)
elif new_album_ranking['type'] == 'artist':
    result = artists.replace_one(filter_criteria, new_album_ranking, upsert=True)
elif new_album_ranking['type'] == 'playlist':
    result = playlists.replace_one(filter_criteria, new_album_ranking, upsert=True)
print(result)

# albums.insert_one(new_album_ranking)
# print(pprint(list(users.find({}))))