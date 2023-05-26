import requests
import time
import os
import hashlib
import json
from dotenv import load_dotenv

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

config_instance = PodcastIndexConfig()
api_key = config_instance.api_key
api_secret = config_instance.api_secret

def create_headers():
        # we'll need the unix time
        epoch_time = int(time.time())

        # our hash here is the api key + secret + time
        data_to_hash = api_key + api_secret + str(epoch_time)

        # which is then sha-1'd
        sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

        # now we build our request headers
        headers = {
            "X-Auth-Date": str(epoch_time),
            "X-Auth-Key": api_key,
            "Authorization": sha_1,
            "User-Agent": "Voyce",
        }
        return headers

def make_request_get_result_helper(url, payload):
    # Perform request
    headers = create_headers()
    result = requests.get(url, headers=headers, params=payload, timeout=5)
    result.raise_for_status()

    # Parse the result as a dict
    result_dict = json.loads(result.text)
    return result_dict

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

def search(query: str, max: int = None, fulltext: bool = False) -> dict:
    # title, author or owner  
      
    url = "https://api.podcastindex.org/api/1.0" + "/search/byterm"

    payload = {"q": query}
    if max is not None:
        payload["max"] = max
    if fulltext:
        payload["fulltext"] = 'fulltext'   # in search by title this is changed to a bool
    
    response = make_request_get_result_helper(url, payload)
    save_output_to_json(response, 'search', 'pi_output_cache/sample_requests_reponses')
    return response

def search_title(query: str, max: int = None, fulltext: bool = False, similar: bool = False) -> dict:
      
    url = "https://api.podcastindex.org/api/1.0" + "/search/bytitle"

    payload = {"q": query}
    if max is not None:
        payload["max"] = max
    if fulltext:
        payload["fulltext"] = True  # in search by title this requires the str 'fulltext'
    if similar:
        payload['similar'] = True
    response = make_request_get_result_helper(url, payload)
    save_output_to_json(response, 'search_title', 'pi_output_cache/sample_requests_reponses')

def search_person(query: str, max: int = None, fulltext: bool = False) -> dict:
    if max is not None and (max < 1 or max > 1000):
        raise ValueError("max must be between 1 and 1000")
    # docs state max 1000 but I'm only getting 100

    #! also seems to privilge title - so 'sandy hook' just gets title with Sandys in
    #! it won't work as an advanced search tool
    
    url = "https://api.podcastindex.org/api/1.0" + "/search/byperson"
    
    payload = {"q": query}
    if max is not None:
        payload["max"] = max
    if fulltext:
        payload["fulltext"] = True  

    response = make_request_get_result_helper(url, payload) 
    save_output_to_json(response, 'search_person', 'pi_output_cache/sample_requests_reponses')


def catergories():
        
    url = "https://api.podcastindex.org/api/1.0" + "/categories/list"

    payload = {}
    
    response = make_request_get_result_helper(url, payload) 
    save_output_to_json(response, 'catergories', 'pi_output_cache/sample_requests_reponses')    

def search_tag(tag: str, max: int = None, start_at: int = None) -> dict:
    
    #! doesn't currently work!  
    
    url = "https://api.podcastindex.org/api/1.0/podcasts/bytag"

    payload = {"tag": tag}
    if max is not None:
        payload["max"] = max
    if start_at is not None:
        payload["start_at"] = start_at
    response = make_request_get_result_helper(url, payload)
    save_output_to_json(response, 'search_tag', 'pi_output_cache/sample_requests_reponses')
    
def search_tag_docs_example():
    url_example = 'https://api.podcastindex.org/api/1.0/podcasts/bytag?podcast-value&max=200&pretty'
    # transcript_test = 'https://api.podcastindex.org/api/1.0/podcasts/bytag?podcast-transcripts&max=200&pretty'
    
    #! From docs: 'This call returns all feeds that support the specified podcast namespace tag.'
    #! Suggests the endpoint works with other podcast namespaces as listed in docs.
    #! However, syntax isn't specified e.g. podcast-value works for what's defined as <podcast:value>
    #! Yet, podcast-transcript or podcast-transcripts doesn't work for <podcast:transcript> etc. 
       
    headers = create_headers()
    response = requests.get(url_example, headers=headers, timeout=20)
    response.raise_for_status()  # Check if the request was successful
    response_json = response.json()  # Get the JSON content of the response
    save_output_to_json(response_json, 'search_tag_docs', 'pi_output_cache/sample_requests_reponses')

def search_medium(medium: str, max: int = None) -> dict:
    valid = ['audiobook', 'blog', 'film', 'music', 'newsletter', 'podcast', 'video']
    if medium not in valid:
        raise ValueError("Invalid medium. Check API docs.")
    if max is not None and (max < 1 or max > 1000):
        raise ValueError("max must be between 1 and 1000")
    
    url = "https://api.podcastindex.org/api/1.0" + "/search/bymedium"
    
    #! HTTPError: 404 Client Error: Not Found for url: 
    #! https://api.podcastindex.org/api/1.0/search/bymedium?medium=film&max=10
    #! Yet this is exactly correct based on the documentation, from the curl example:
    #! "https://api.podcastindex.org/api/1.0/podcasts/bymedium?medium=film&max=10"
       
    
    payload = {"medium": medium}
    if max is not None:
        payload["max"] = max
    
    response = make_request_get_result_helper(url, payload) 
    save_output_to_json(response, 'search_medium', 'pi_output_cache/sample_requests_reponses')

def trending_pods(max: int = None, since: int = None, lang: str = None, cat: str = None, notcat: str = None) -> dict:
      
    url = "https://api.podcastindex.org/api/1.0/podcasts/trending"
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

    response = make_request_get_result_helper(url, payload)
    save_output_to_json(response, 'recent_eps', 'pi_output_cache/sample_requests_reponses')

def ep_by_ep_id():
    pass

def eps_by_feed_id(query: str, max: int = None, fulltext: bool = False, similar: bool = False) -> dict:
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
    response = make_request_get_result_helper(url, payload)
    # save_output_to_json(response, 'ep_by_ep_id', 'pi_output_cache/sample_requests_reponses')
    return response

def eps_recent():
    pass

def feeds_recent():
    # presumably this is just the feeds equivalent of episodes
    pass

def new_feeds():
    # or use feed data which is the same but works on PI date, rather than the podcasts internal timestamp
    pass


def fetch_all():
    search("Python", max=3, fulltext='fulltext')
    search_title("JavaScript", max=3, fulltext=True, similar=True)
    search_person("Johnny Depp", max=1000, fulltext=True)
    catergories()
    # search_tag("podcast-value", max=20) #! NOT WORKING
    # search_tag_docs_example() #! NOT WORKING
    # search_medium('film', max=10) #! NOT WORKING
    print("All API calls extracted")
    return True

# fetch_all()
print(eps_by_feed_id(742305))



