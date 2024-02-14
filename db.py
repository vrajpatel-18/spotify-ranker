from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import json
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
login_string = os.environ.get("MONGO_LOGIN")
client = MongoClient(login_string)

db = client.get_database('SpotifyRanker')
users = db.users
albums = db.albums
artists = db.artists
playlists = db.playlists


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



def save_ranking(data):
    # add album to user's rankings array
    users.update_one({'id': data['user_id']}, {"$pull": {"rankings": {"id": data["id"]}}})
    users.update_one({'id': data['user_id']}, {'$push': {'rankings': data}})
    
    # add album to user's rankings_history
    users.update_one({'id': data['user_id']}, {"$pull": {f"rankings_history.{data['id']}": {"rank_date": data['rank_date']}}})
    users.update_one({'id': data['user_id']}, {"$push": {f"rankings_history.{data['id']}": data}})
    
    # add album to albums collection
    filter_criteria = {
        "id": data['id'],
        "user_id": data['user_id']
    }
    albums.replace_one(filter_criteria, data, upsert=True)
    
# new_album_ranking = {
#     'id': '0On7uutIu9rZRvP9aJbMog',
#     'unranked': [],
#     'ranked': [
#         "2HALQBSAvpw1oCzL5QsrT2",
#         "08YvUaUsZktAG6zEMDwUqO",
#         "00ZQQArUJReFfsMnl8dIgd",
#         "2VjOTvl50tscmc0RDjPdr2"
#     ],
#     'type': 'album',
#     'user_id': 'vrajiepoo'
# }


def get_ranking(user_id, ranking_id):
    raw_data = users.find_one({'id': user_id}, {'rankings': {'$elemMatch': {'id': ranking_id}}})
    if len(raw_data) == 1:
        return {'status': 'error', 'message': 'No ranking found'}
    data = {
        'unranked': raw_data['rankings'][0]['unranked'],
        'ranked': raw_data['rankings'][0]['ranked'],
        'status': 'success'
    }
    return data