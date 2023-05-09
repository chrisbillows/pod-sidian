import json
import os
from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI, OutputHandler

'''
    Takes JSON of tracked podcasts and searches for new episodes by feed id.

    It updates a second JSON with the new episodes.
'''

# dummy podcast search API call

tracked_pods_json = 'tracked_pods_jsons/002_pods_from_json.json'

with open(tracked_pods_json, 'r') as f:
    json_data = f.read()
    tracked_pods = json.loads(json_data)

def api_call(pod_id):
    config = PodcastIndexConfig()
    api_instance = PodcastIndexAPI(config.config)
    recent_episdes = api_instance.index.episodesByFeedId(pod_id, max_results=5)
    return recent_episdes

for podcast in tracked_pods['podcasts being tracked']:
        pod_id = podcast['id']
        print(podcast['title'], pod_id)
        print(f"Saved episodes before: {[episode['id'] for episode in podcast['episodes']]}")
        print("------------")

        api_payload = api_call(pod_id)
        recent_episodes = api_payload['items']

        saved_episode_ids = [episode["id"] for episode in podcast["episodes"]]
        
        for recent_episode in recent_episodes:
            if recent_episode["id"] not in saved_episode_ids:
                podcast["episodes"].append(recent_episode)
        
        sorted_episodes = sorted(podcast["episodes"], key=lambda x: x['id'], reverse=True)
        podcast["episodes"] = sorted_episodes

        print(f"Saved episodes after: {[episode['id'] for episode in podcast['episodes']]}")
        print()
        print()


with open(('tracked_pods_jsons/003_update_002_from_api.json'), "w") as f:
    json.dump(tracked_pods, f, indent=4)
    print("Tracked pods UPDATED!")



    