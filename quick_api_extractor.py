from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI, OutputHandler

config = PodcastIndexConfig()
api_instance = PodcastIndexAPI(config.config)

talk_python_feed_id = 742305
python_bites_feed_id = 1021771
real_python_feed_id = 436512
daily_tech_news_id = 586839

results = api_instance.index.episodesByFeedId(talk_python_feed_id, max_results=20)
OutputHandler.save_output_to_json(results, 'talk__python', 'pi_output_cache/episode_for_track_pod')
print("Success!")