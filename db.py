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
feedback = db.feedback


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
    
    # Modify user's rankings_history based on new logic
    user_id = data['user_id']
    ranking_id = data['id']
    
    # Retrieve the most recent ranking from rankings_history for comparison
    user = users.find_one({'id': user_id}, {f'rankings_history.{ranking_id}': 1})
    rankings_history = user.get('rankings_history', {}).get(ranking_id, [])
    
    # Check if there's a most recent ranking to compare with
    if rankings_history:
        last_ranking = rankings_history[-1]  # Get the most recent ranking
        # Compare both 'unranked' and 'ranked' lists in the new and most recent rankings
        if (last_ranking.get('unranked', []) == data.get('unranked', []) and
            last_ranking.get('ranked', []) == data.get('ranked', [])):
            # If identical, do not update rankings_history
            print("Ranking is identical to the most recent one. Not adding to rankings_history.")
        else:
            # If different, update rankings_history
            users.update_one({'id': user_id}, {"$push": {f"rankings_history.{ranking_id}": data}})
            print("Ranking is different. Added to rankings_history.")
    else:
        # If no previous rankings, just add the new ranking
        users.update_one({'id': user_id}, {"$push": {f"rankings_history.{ranking_id}": data}})
        print("No previous rankings. Added to rankings_history.")
    
    # add album to albums collection
    filter_criteria = {
        "id": data['id'],
        "user_id": data['user_id']
    }
    if data['type'] == 'album':
        albums.replace_one(filter_criteria, data, upsert=True)
    elif data['type'] == 'artist':
        artists.replace_one(filter_criteria, data, upsert=True)
    elif data['type'] == 'playlist':
        playlists.replace_one(filter_criteria, data, upsert=True)

    
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
#     'rank_date': '2021-08-01'
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



def give_feedback(message):
    feedback.insert_one({'message': message})
    return {'status': 'success'}