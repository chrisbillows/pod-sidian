import datetime
from dotenv import load_dotenv
import json
import os
import podcastindex
from bs4 import BeautifulSoup
import textwrap

# class PodcastIndexConfig:
#     def __init__(self):
#         self.load_environment_variables()
#         self.api_key = os.getenv("podcast_index_api_key")        
#         self.api_secret = os.getenv("podcast_index_secret")
#         self.config = {
#             "api_key": self.api_key,
#             "api_secret": self.api_secret
#         }
    
#     @staticmethod
#     def load_environment_variables():
#         load_dotenv()

# config_instance = PodcastIndexConfig()

# index = podcastindex.init(config_instance.config)
# results = index.episodesByFeedId(742305, max_results=10)

#! Read results
file_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/pi_output_cache/episode_for_track_pod/001_talk_python_last_23.json"
with open(file_path, 'r') as json_file:
    dummy_api_response = json.load(json_file)

data = dummy_api_response['items']

# placeholder, will be available in search/saved pod, so pass to this function
feed_title = "Talk Python To Me"

print("\n-------------------")
print(feed_title.upper())
print("-------------------\n")

for podcast in data:
    ep_num = podcast['episode']
    ep_title = podcast['title']
    ep_date = podcast['datePublishedPretty']
    ep_duration_seconds = podcast['duration']
        
    description = podcast["description"]
    soup = BeautifulSoup(description, "html.parser")
    text = soup.get_text("\n")
    description_clean = "\n\n".join(line.strip() for line in text.split("\n") if line.strip())
    terminal_width = os.get_terminal_size().columns
    description_wrapped = "\n".join(textwrap.fill(line, width=terminal_width) for line in description_clean.split("\n"))    

    formatted_ep_link = f'\033]8;;{podcast["link"]}\007{podcast["link"]}\033]8;;\007'
    formatted_ep_mp3 = f'\033]8;;{podcast["enclosureUrl"]}\007{podcast["enclosureUrl"]}\033]8;;\007'
    
    print(f"{ep_num} - {ep_title.upper()}")
    print("--------------------------------------")
    print(f"Release date:     {ep_date}")
    print(f"Duration:         {int(ep_duration_seconds/60)} mins")
    print(f"Episode Page:     {formatted_ep_link}")
    print(f"Download link:    {formatted_ep_mp3}\n")
    print(description_wrapped)
    print()







