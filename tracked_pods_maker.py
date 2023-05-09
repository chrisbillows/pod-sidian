import json
import os
import datetime

'''
Working from saved JSONs this quickly creates a tracked_pods dictionary of three podcasts. 

For testing episode downloading and overall data formatting.

Saves the file to to 'tracked_pods_jsons/002_pods_from_json'.
'''


# empty JSON
tracked_pods_dict = {
        "podcasts being tracked": 
        [
    ]
}

# dummy podcast search API call
pod_search_results = 'pi_output_cache/sample_api_responses/001_search.json'

with open(pod_search_results, 'r') as f:
    json_data = f.read()
    data = json.loads(json_data)

# LIST of podcasts returned by search
new_podcasts = data['feeds']

# indexes of three to track
talk_python = new_podcasts[0]
python_bites = new_podcasts[1]
real_python = new_podcasts[3]

# locate JSON list for saving podcasts - LIST
tracked_pods_list = tracked_pods_dict['podcasts being tracked']

# add sample pods
tracked_pods_list.append(talk_python)
tracked_pods_list.append(python_bites)
tracked_pods_list.append(real_python)

# create an empty episode list for saving episodes
for podcast in tracked_pods_list:
    podcast['episodes'] = []
    podcast['dateTracked'] = datetime.datetime.now()   
    podcast['dateTrackedPretty'] = podcast['dateTracked'].strftime("%Y-%m-%d %H:%M:%S")  

# --- display to see it's working ---
# for podcast in tracked_pods_list:
#     print(podcast['title'], podcast['id'])
#     print(podcast['episodes'])

# --- add some dummy data ---
# tracked_pods_list[0]['episodes'].append({'test_episode': 107})
# tracked_pods_list[0]['episodes'].append({'test_episode': 122, 'info': 'some more info'})

# dummy episode search API call for TALK PYTHON TO ME
recent_talk_py_eps = './pi_output_cache/episode_for_track_pod/001_talk_python_last_23.json'

with open(recent_talk_py_eps, 'r') as f:
    json_data = f.read()
    payload = json.loads(json_data)

# LIST of episodes
talk_py_eps = payload['items']

# SLICE for smaller sample
sample_talk_py_eps = talk_py_eps

# append to JSON
tracked_pods_list[0]['episodes'].extend(sample_talk_py_eps)

# --- display JSON --- 
# print(tracked_pods_dict)

# create list of tracked episode ids
talk_python = tracked_pods_dict['podcasts being tracked'][0]
saved_eps = talk_python['episodes']

# --- print saved episode ids ---
# for episode in talk_python['episodes']:
#     print(episode['episode'])
#     print(episode['id'])


# --- loop to create iterated outputs
# output_directory = 'tracked_pods_jsons'
# file_name = 'pods_from_json'

# os.makedirs(output_directory, exist_ok=True)

# file_number = 1
# while True:
#     output_file = f"{file_number:03d}_{file_name}.json"
#     existing_files = os.listdir(output_directory)

#     file_exists = False
#     for file in existing_files:
#         if file.startswith(f"{file_number:03d}_"):
#             file_exists = True
#             break

#     if not file_exists:
#         break

#     file_number += 1

with open(('tracked_pods_jsons/002_pods_from_json.json'), "w") as f:
    json.dump(tracked_pods_dict, f, indent=4)
    print("Tracked_pods_saved")














