import datetime
import hashlib
import json
import os
from typing import Dict, Any
import warnings

import requests
from dotenv import load_dotenv


class OutputSaver:
    
    """
    A class to save Podcast Index API outputs.
    The root directory is "cache" and is not alterable.
    
    Attributes:
        output_main_dir (str): Main directory for output files. The full path will be 
            "cache/output_main_dir". Default is "podcast_index_outputs".
        output_sub_dir (str): Subdirectory for output files. The full path will be 
            "cache/output_main_dir/output_sub_dir". Default is "temp".

    Args:
        output_main_dir (str, optional): Main directory for output files. Defaults to 
            "podcast_index_outputs".
        output_sub_dir (str, optional): Subdirectory for output files. Defaults to "temp".
        
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
    A class to create the required headers to access the Podcast Index API.
    
    The class uses environment variables to fetch API credentials and uses them to create
    the headers required for API requests.

    Attributes:
        api_key (str): API key retrieved from the environment variables. 
        api_secret (str): API secret retrieved from the environment variables.
        headers (dict): The headers to be used for API requests, created using 
            the API key and secret.
            
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
    A class to handle API requests to Podcast Index endpoints.

    Class methods are organised in the same order as Podcast Index docs.
    Note that not all API available endpoints are covered.

    Attributes:
        headers (dict): A PodcastIndexConfig.headers instance variable. 

    Args:
        headers (dict): The headers used for API requests.
        
    """
   
    def __init__(self, headers) -> None:
        self.headers = headers

    def search(self, query: str, max: int = None, fulltext: bool = False) -> dict:
        """
        Searches podcasts by term. Searched fields are title, owner and author. 
        (Use search_by_title for a pure title search)

        The search can be customized with the optional `max` and `fulltext` parameters.

        Args:
            query (str): The term to search for.
            
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be 60.
                Defaults to None, in which case the API's default maximum is used.
            
            fulltext (bool, optional): Return the full text value of any text fields (ex: description). 
                If not provided, text field values are truncated to 100 words. If True, the string 
                'fulltext' is added to the payload. Defaults to False.
                
                Note the API requires a str 'fulltext' and not the bool used here.

        Returns:
            dict: The search results, in the form returned by the API.

        """
       
        # title, author or owner  
        # docs state max = 1000 but I've been getting max = 60

        url = "https://api.podcastindex.org/api/1.0" + "/search/byterm"
        
        payload = {"q": query}
        
        if max is not None:
            payload["max"] = max
        
        if fulltext:
            payload["fulltext"] = 'fulltext'   # in search_by_title this is changed to an actual bool
        
        response = self._make_request_get_result_helper(url, payload)
        
        return response

    def search_by_title(self, query: str, max: int = None, fulltext: bool = False, similar: bool = False) -> dict:
        """
        Searches podcasts by term. Searched fields are title only. 
        (Use search for title, owner and author). 
        
        IN LIMITED TESTING THE SEARCH RESULTS WERE LESS USEFUL THAT 'search'. Use 'search' for now.        
                
        The search can be customized with the optional `max`, `fulltext` and `similar` parameters.

        Args:
            query (str): The term to search for.
            
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be 60.
                Defaults to None, in which case the API's default maximum is used.
            
            fulltext (bool, optional): Return the full text value of any text fields (ex: description). 
                If not provided, text field values are truncated to 100 words. If True, the string 
                'fulltext' is added to the payload. Defaults to False.
            
            similar (bool, optional): Return results for similar.  e.g. perhaps JavaScript for javascript. 
                Available, although has made little difference in limited testing. Defaults to False.

        Returns:
            dict: The search results, in the form returned by the API.

        """
        
        warnings.warn("The 'search_by_title' method utilise an endpoint that may be unreliable. This method is therefore deprecated and may be removed in a future version", DeprecationWarning)
                
        url = "https://api.podcastindex.org/api/1.0" + "/search/bytitle"
        
        payload = {"q": query}
        
        if max is not None:
            payload["max"] = max
        
        if fulltext:
            payload["fulltext"] = True  # in search this requires the str 'fulltext', not a bool
        
        if similar:
            payload['similar'] = True
        
        response = self._make_request_get_result_helper(url, payload)
        
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
        return response

    def categories(self):
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
    
    def multi_search_multi_endpoints(self, searches: list, json_maker: OutputSaver) -> bool:
        for s in searches:
            try:
                s_filename = s.replace(' ', '_')
                search_payload = self.search(s)
                search_by_title_payload = self.search_by_title(s)
                json_maker.save_output_to_json(search_payload, f"search_{s_filename}")
                json_maker.save_output_to_json(search_by_title_payload, f"search_by_title{s_filename}")
                print(f"JSONS for {s} created.")
            except Exception as e:
                print(f"Error occurred: {e}")
                return False
        return True

    def fetch_all(self):

        payloads = {
            'search': self.search("True Crime",500, True),
            'categories': self.categories()
        }

        json_maker = OutputSaver(output_sub_dir="sample_set")

        for method_name, payload in payloads.items():
            json_maker.save_output_to_json(payload, method_name)
        print("Sample API calls extracted")
    
        return True

    def _make_request_get_result_helper(self, url, payload):
        headers = self.headers
        result = requests.get(url, headers=headers, params=payload, timeout=5)
        result.raise_for_status()
        result_dict = json.loads(result.text)
        return result_dict


if __name__ == "__main__":
    
    config = PodcastIndexConfig()
    podcast_index_instance = PodcastIndexService(config.headers)
    json_maker = OutputSaver()


     
    # TODO so this works great - I need to make sure all the methods are working


    # config = PodcastIndexConfig()
    # podcast_index_instance = PodcastIndexService(config.headers)
    # podcast_index_instance.fetch_all()
    
  

    