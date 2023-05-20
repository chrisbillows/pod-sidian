from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI, OutputHandler
import podcastindex 
import json

#! podcast index setup

# config = {
#     "api_key": 'HXCG8NBSHZAG7WYFWHQV',
#     "api_secret": 'WnkCGw5QWPy3Q9DugJ^vwBPfHgjmEQUAm9Wvs^ZB'
# }
# index = podcastindex.init(config)
# results = index.episodesByFeedId(742305, max_results=22)
# OutputHandler.save_output_to_json(results, 'talk_python_last_23', 'pi_output_cache/episode_for_track_pod')

# file_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/pi_output_cache/episode_for_track_pod/001_talk_python_last_23.json"
# with open(file_path, 'r') as json_file:
#     dummy_api_response = json.load(json_file)

# data = dummy_api_response['items']

#! my pointless wrappers

config = PodcastIndexConfig()
api_instance = PodcastIndexAPI(config.config)

talk_python_feed_id = 742305
python_bites_feed_id = 1021771
real_python_feed_id = 436512
daily_tech_news_id = 586839

results = api_instance.index.episodesByFeedId(talk_python_feed_id, max_results=20)
OutputHandler.save_output_to_json(results, 'talk__python', 'pi_output_cache/episode_for_track_pod')
print("Success!")