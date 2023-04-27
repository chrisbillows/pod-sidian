import datetime
from dotenv import load_dotenv
import json
import os
import re

import podcastindex


class ValidQueriesExtractor:
    '''
    A class to create a dictionary of valid queries (strings and ids) required for each available API call in python-podcastindex.

    For use by APICacher to create a cached JSON of each API call's output.
    
    Extracts feed_id, itunes_id, and feed_url from a payload of trending podcasts, returning the results from the first podcast 
    with three valid outputs for those fields.

    It also extracts episode_id from a payload of recent episodes, returning the result from the first episode with a valid output for 
    that field. 

    Three constants: SEARCH_TERM, SEARCH_PERSON and MAX complete the required query variables for all the availble API calls.
    '''

    SEARCH_TERM = 'python'
    SEARCH_PERSON = 'Guido van Rossum'
    MAX = 10 

    def __init__(self, api_instance):
        self.valid_queries = {'search_term': self.SEARCH_TERM, 'person': self.SEARCH_PERSON, 'max': self.MAX}
        self.api_instance = api_instance

    def get_all_valid_fields(self):
        self.get_podcast_fields()
        self.get_episode_field()
        return self.valid_queries

    def get_podcast_fields(self):
        # with open('documenting_pi_api/payload_examples/011_trendingPodcasts.json', 'r') as file:
        #     payload = json.load(file)
        payload = self.api_instance.index.trendingPodcasts(10)

        podcasts = payload['feeds']

        for podcast in podcasts:
            feed_id = podcast['id']
            itunes_id = podcast['itunesId']
            feed_url = podcast['url']

            if self.is_valid_id(feed_id, itunes_id) and self.is_valid_url(feed_url):
                self.valid_queries.update ({'feed_id': feed_id, 'itunes_id': itunes_id, 'feed_url': feed_url})
                return self.valid_queries
        else:
            return "No valid data" 
            
    def get_episode_field(self):
        # with open('documenting_pi_api/payload_examples/006_episodesByFeedId.json', 'r') as file:
        #     payload = json.load(file)
        payload = self.api_instance.index.recentEpisodes(10)
        
        episodes = payload['items']
        
        for episode in episodes:
            episode_id = episode['id']
            if self.is_valid_id(episode_id):
                self.valid_queries['episode_id'] = episode_id
                return self.valid_queries
        else:
            return "No valid data" 

    def is_valid_id(self, *args):
        for arg in args:
            if not isinstance(arg, int) or arg is None:
                return False
        return True

    def is_valid_url(self, url):
        url_pattern = re.compile(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )
        if not isinstance(url, str) or not url_pattern.match(url):
            return False
        else:
            return True


class BatchAPICaller():

    API_CALLS_DICT = {
    'search': {'query_type': 'search_term', 'main_data_field': 'feeds'},
    'podcastByFeedUrl': {'query_type': 'feed_url', 'main_data_field': 'feed'},
    'podcastByFeedId': {'query_type': 'feed_id', 'main_data_field': 'feed'},
    'podcastByItunesId': {'query_type': 'itunes_id', 'main_data_field': 'feed'},
    'episodesByFeedUrl': {'query_type': 'feed_url', 'main_data_field': 'items'},
    'episodesByFeedId': {'query_type': 'feed_id', 'main_data_field': 'items'},
    'episodesByItunesId': {'query_type': 'itunes_id', 'main_data_field': 'items'},
    'episodeById': {'query_type': 'episode_id', 'main_data_field': 'episode'},
    'episodesByPerson': {'query_type': 'person', 'main_data_field': 'items'},
    'recentEpisodes': {'query_type': 'max', 'main_data_field': 'items'},
    'trendingPodcasts': {'query_type': 'max', 'main_data_field': 'feeds'}
}
    
    def __init__(self, api_instance, valid_query_set):
        self.api_instance = api_instance
        self.valid_query_set = valid_query_set


    def download_sample_set(self):
        output_directory = "pi_output_cache/sample_api_responses"
        for method, query_info in BatchAPICaller.API_CALLS_DICT.items():
            query = self.valid_query_set[query_info['query_type']]
            method_to_call = getattr(self.api_instance.index, method)
            payload = method_to_call(query)
            print(f"For the method {method} -- the query type used: {query_info['query_type']} -- the query: {query}")
            OutputHandler.save_output_to_json(payload, method, output_directory)


class PodcastIndexConfig:
    def __init__(self):
        self.load_environment_variables()
        self.api_key = os.getenv("podcast_index_api_key")        
        self.api_secret = os.getenv("podcast_index_secret")
        self.config = {
            "api_key": self.api_key,
            "api_secret": self.api_secret
        }
    
    @staticmethod
    def load_environment_variables():
        load_dotenv()


class PodcastIndexAPI:
    '''
    A class to represent an instance of a Podcast Index API call. Podcast methods return summary data for an entire podcast.    
    Episode methods return summary data for individual episodes. Every method has a paramenter 'output' that takes a boolean
    (default=False) to allow caching to JSON.
   '''
    def __init__(self, config):
        self.config = config
        self.index = podcastindex.init(config)
    
    def fetch_podcasts_by_string(self, name, output=False):
        '''
        Podcast method. search the podcast index api for podcast summary data. Returns a python direction. Podcast Index applies search string
        to title, author and owner fields.

         Parameters:
        - name (str): The search string to query.
        - output (bool): If True, save the output to a JSON file. Default is False.

        Returns:
        - result (dict): A dictionary containing the search results.

        '''   
        result = self.index.search(name, clean=False)
        if output:
            OutputHandler.save_output(result)
        return result

    def validate_podcast_id(self, id, output=False):
        '''
        Podcast method. Search the podcast index by single podcast ID. Used to check a podcast ID is correct.
        '''
        result = self.index.podcastByFeedId(id)
        if output:
            OutputHandler.save_output(result)
        return result
        
    def fetch_episodes_by_id(self, podcast_id, weeks=None, episode_id=None, output=False):
        if weeks is not None:
            week_in_seconds = -604800  # 60 * 60 * 24 * 7
            since = weeks * week_in_seconds
        else:
            since = None

        if episode_id is not None:
            result = self.index.episodeById(episode_id)
        else:
            result = self.index.episodesByFeedId(podcast_id, since=since)

        if output:
            OutputHandler.save_output(result)
        return result


class OutputHandler:
    @staticmethod
    def save_output_to_json(payload, method, output_directory):
        output_directory = output_directory
        os.makedirs(output_directory, exist_ok=True)
       
        file_number = 1
        while True:
            output_file = f"{file_number:03d}_{method}.json"
            existing_files = os.listdir(output_directory)
    
            file_exists = False
            for file in existing_files:
                if file.startswith(f"{file_number:03d}_"):
                    file_exists = True
                    break

            if not file_exists:
                break

            file_number += 1

        with open(os.path.join(output_directory, output_file), "w") as f:
            json.dump(payload, f, indent=4)


class DataProcessor:
    @staticmethod
    def convert_unix_time(time_unix):
        date_time = datetime.datetime.fromtimestamp(time_unix)
        human_readable = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return human_readable


class DummyPodcastIndexAPI:
    '''
    For testing. 
    '''
    @staticmethod
    def dummy_fetch_podcasts_by_string():
        #TODO create for testing
        pass
        

