import datetime
import hashlib
import json
import os
from typing import Dict, Any

import requests
from dotenv import load_dotenv


class OutputSaver:
    """
    A class to save Podcast Index API outputs to the cache directory.
    
    The class paremeters are 
    a) output directory with a default of "podcast_index_outputs"
    b) output sub directory with a default of "temp"
           
    """

    def __init__(self, output_main_dir="podcast_index_outputs", output_sub_dir="temp"):
        self.output_main_dir = output_main_dir
        self.output_sub_dir = output_sub_dir
        
    def save_output_to_json(self, payload: Dict[str, Any], method_name:str) -> None :
        file_number = 1
        while True:
            time = datetime.datetime.now().strftime("%Y%m%d %H%M")
            output_file = f"{file_number:03d}_{method_name}_{time}.json"
            output_dir = os.path.join("cache", self.output_main_dir, self.output_sub_dir)
            os.makedirs(output_dir, exist_ok=True)
            existing_files = os.listdir(output_dir)

            file_exists = False
            for file in existing_files:
                if file.startswith(f"{file_number:03d}_"):
                    file_exists = True
                    break

            if not file_exists:
                break

            file_number += 1

        with open(os.path.join(output_dir, output_file), "w") as f:
            json.dump(payload, f, indent=4)



class PodcastIndexConfig:
    
    """
    A class to create the required headers to access the API.
    """   
    
    def __init__(self) -> None:
        self._load_environment_variables()
        self.api_key = os.getenv("podcast_index_api_key")        
        self.api_secret = os.getenv("podcast_index_secret")
        self.headers = self._create_headers()
        
    @staticmethod
    def _load_environment_variables():
        load_dotenv()

    def _create_headers(self):
            epoch_time = int(datetime.datetime.now().timestamp())
            data_to_hash = self.api_key + self.api_secret + str(epoch_time)
            sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
            headers = {
                "X-Auth-Date": str(epoch_time),
                "X-Auth-Key": self.api_key,
                "Authorization": sha_1,
                "User-Agent": "Voyce",
            }
            return headers


class PodcastIndexService:
    
    """
    A class to handle API requests to selected Podcast Index endpoints.
    """
    def __init__(self, headers) -> None:
        self.headers = headers

    def search(self, query: str, max: int = None, fulltext: bool = False) -> dict:
        # title, author or owner  
        url = "https://api.podcastindex.org/api/1.0" + "/search/byterm"
        payload = {"q": query}
        if max is not None:
            payload["max"] = max
        if fulltext:
            payload["fulltext"] = 'fulltext'   # in search by title this is changed to a bool
        response = self._make_request_get_result_helper(url, payload)
        # save_output_to_json(response, 'search', 'pi_output_cache/sample_requests_reponses')
        return response

    def search_title(self, query: str, max: int = None, fulltext: bool = False, similar: bool = False) -> dict:
        url = "https://api.podcastindex.org/api/1.0" + "/search/bytitle"
        payload = {"q": query}
        if max is not None:
            payload["max"] = max
        if fulltext:
            payload["fulltext"] = True  # in search by title this requires the str 'fulltext'
        if similar:
            payload['similar'] = True
        response = self._make_request_get_result_helper(url, payload)
        # save_output_to_json(response, 'search_title', 'pi_output_cache/sample_requests_reponses')
        return response

    def search_person(self, query: str, max: int = None, fulltext: bool = False) -> dict:
        if max is not None and (max < 1 or max > 1000):
            raise ValueError("max must be between 1 and 1000")
        # docs state max 1000 but I'm only getting 100
        # Won't work as an advanced search tool - seems to privilege title field 
        # e.g. 'sandy hook' gets podcasts titled "Sandy etc" not where Sandy Hook is mentioned in the description
        url = "https://api.podcastindex.org/api/1.0" + "/search/byperson"
        payload = {"q": query}
        if max is not None:
            payload["max"] = max
        if fulltext:
            payload["fulltext"] = True  
        response = self._make_request_get_result_helper(url, payload) 
        # save_output_to_json(response, 'search_person', 'pi_output_cache/sample_requests_reponses')
        return response

    def catergories(self):
        url = "https://api.podcastindex.org/api/1.0" + "/categories/list"
        payload = {}
        response = self._make_request_get_result_helper(url, payload) 
        # save_output_to_json(response, 'catergories', 'pi_output_cache/sample_requests_reponses')  
        return response  
        
    def trending_podcasts(self, max: int = None, since: int = None, lang: str = None, cat: str = None, notcat: str = None) -> dict:
        url = "https://api.podcastindex.org/api/1.0" + "/podcasts/trending"
        # "https://api.podcastindex.org/api/1.0/podcasts/trending?max=10&since=1612125785&lang=en&cat=News&notcat=News"
        payload = {}
        if max is not None:
            payload["max"] = max
        if since is not None:
            payload["since"] = since
        if lang is not None:
            payload["lang"] = lang
        if cat is not None:
            payload["cat"] = cat
        if notcat is not None:
            payload["notcat"] = notcat
        response = self._make_request_get_result_helper(url, payload)
        # save_output_to_json(response, 'recent_eps', 'pi_output_cache/sample_requests_reponses')
        return response

    def episode_by_episode_id(self):
        pass

    def episodes_by_feed_id(self, query: str, max: int = None, fulltext: bool = False, similar: bool = False) -> dict:
        # may want to use eps recent
        # seems to duplicate functionality but that allows a cut off by EPISODE
        url = "https://api.podcastindex.org/api/1.0" + "/episodes/byfeedid"
        payload = {"id": query}
        if max is not None:
            payload["max"] = max
        if fulltext:
            payload["fulltext"] = True  # in search by title this requires the str 'fulltext'
        if similar:
            payload['similar'] = True
        response = self._make_request_get_result_helper(url, payload)
        # save_output_to_json(response, 'ep_by_ep_id', 'pi_output_cache/sample_requests_reponses')
        return response

    def eps_recent(self):
        pass

    def feeds_recent(self):
        # presumably this is just the feeds equivalent of episodes
        pass

    def new_feeds(self):
        # or use feed data which is the same but works on PI date, rather than the podcasts internal timestamp
        pass

    def fetch_all(self):
        json_maker = OutputSaver()
        
        self.search("Python", max=3, fulltext='fulltext')
        self.search_title("JavaScript", max=3, fulltext=True, similar=True)
        self.search_person("Johnny Depp", max=1000, fulltext=True)
        self.catergories()
        print("Sample API calls extracted")
        return True

    def _make_request_get_result_helper(self, url, payload):
        headers = self.headers
        result = requests.get(url, headers=headers, params=payload, timeout=5)
        result.raise_for_status()
        result_dict = json.loads(result.text)
        return result_dict
    
        # CHAT GPT SUGGESTION to save many payloads 
        # config = PodcastIndexConfig()

        # podcast_index_instance = PodcastIndexService(config.headers)
    
        # payloads = {
        #     'search': podcast_index_instance.search("True Crime",500, True),
        #     'categories': podcast_index_instance.categories(),
        #     # Add more payloads here as needed
        # }

        # json_maker = OutputSaver()

        # for method_name, payload in payloads.items():
        #     json_maker.save_output_to_json(payload, method_name)


if __name__ == "__main__":
    config = PodcastIndexConfig()

    podcast_index_instance = PodcastIndexService(config.headers)
   
    search = podcast_index_instance.search("True Crime", 500, True)
    catergories = podcast_index_instance.catergories()

    json_maker = OutputSaver()

    json_maker.save_output_to_json(search, 'search')
    json_maker.save_output_to_json(catergories, 'catergories')
     
    # TODO so this works great - I need to make sure all the methods are working

  
    # podcast_index_instance.fetch_all()
    # print("All API examples fetched and stored")
   

    