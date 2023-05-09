import requests
import time
import hashlib
import json

from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI

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
    result = requests.post(url, headers=headers, data=payload, timeout=5)
    result.raise_for_status()

    # Parse the result as a dict
    result_dict = json.loads(result.text)
    return result_dict

def search(query, clean=False):
       
    # Setup request
    url = "https://api.podcastindex.org/api/1.0" + "/search/byterm"

    # Setup payload
    payload = {"q": query}
    if clean:
        payload["clean"] = 1

    # Call Api for result
    return make_request_get_result_helper(url, payload)

def catergories():
    # url = https://api.podcastindex.org/api/1.0/categories/list?pretty
    
    # Setup request
    url = "https://api.podcastindex.org/api/1.0" + "/categories/list"

    # Setup payload
    payload = {}
    
    # Call Api for result
    return make_request_get_result_helper(url, payload)

# print(catergories())

payload = {'status': 'true', 'feeds': [{'id': 1, 'name': 'Arts'}, {'id': 2, 'name': 'Books'}, {'id': 3, 'name': 'Design'}, {'id': 4, 'name': 'Fashion'}, {'id': 5, 'name': 'Beauty'}, {'id': 6, 'name': 'Food'}, {'id': 7, 'name': 'Performing'}, {'id': 8, 'name': 'Visual'}, {'id': 9, 'name': 'Business'}, {'id': 10, 'name': 'Careers'}, {'id': 11, 'name': 'Entrepreneurship'}, {'id': 12, 'name': 'Investing'}, {'id': 13, 'name': 'Management'}, {'id': 14, 'name': 'Marketing'}, {'id': 15, 'name': 'Non-Profit'}, {'id': 16, 'name': 'Comedy'}, {'id': 17, 'name': 'Interviews'}, {'id': 18, 'name': 'Improv'}, {'id': 19, 'name': 'Stand-Up'}, {'id': 20, 'name': 'Education'}, {'id': 21, 'name': 'Courses'}, {'id': 22, 'name': 'How-To'}, {'id': 23, 'name': 'Language'}, {'id': 24, 'name': 'Learning'}, {'id': 25, 'name': 'Self-Improvement'}, {'id': 26, 'name': 'Fiction'}, {'id': 27, 'name': 'Drama'}, {'id': 28, 'name': 'History'}, {'id': 29, 'name': 'Health'}, {'id': 30, 'name': 'Fitness'}, {'id': 31, 'name': 'Alternative'}, {'id': 32, 'name': 'Medicine'}, {'id': 33, 'name': 'Mental'}, {'id': 34, 'name': 'Nutrition'}, {'id': 35, 'name': 'Sexuality'}, {'id': 36, 'name': 'Kids'}, {'id': 37, 'name': 'Family'}, {'id': 38, 'name': 'Parenting'}, {'id': 39, 'name': 'Pets'}, {'id': 40, 'name': 'Animals'}, {'id': 41, 'name': 'Stories'}, {'id': 42, 'name': 'Leisure'}, {'id': 43, 'name': 'Animation'}, {'id': 44, 'name': 'Manga'}, {'id': 45, 'name': 'Automotive'}, {'id': 46, 'name': 'Aviation'}, {'id': 47, 'name': 'Crafts'}, {'id': 48, 'name': 'Games'}, {'id': 49, 'name': 'Hobbies'}, {'id': 50, 'name': 'Home'}, {'id': 51, 'name': 'Garden'}, {'id': 52, 'name': 'Video-Games'}, {'id': 53, 'name': 'Music'}, {'id': 54, 'name': 'Commentary'}, {'id': 55, 'name': 'News'}, {'id': 56, 'name': 'Daily'}, {'id': 57, 'name': 'Entertainment'}, {'id': 58, 'name': 'Government'}, {'id': 59, 'name': 'Politics'}, {'id': 60, 'name': 'Buddhism'}, {'id': 61, 'name': 'Christianity'}, {'id': 62, 'name': 'Hinduism'}, {'id': 63, 'name': 'Islam'}, {'id': 64, 'name': 'Judaism'}, {'id': 65, 'name': 'Religion'}, {'id': 66, 'name': 'Spirituality'}, {'id': 67, 'name': 'Science'}, {'id': 68, 'name': 'Astronomy'}, {'id': 69, 'name': 'Chemistry'}, {'id': 70, 'name': 'Earth'}, {'id': 71, 'name': 'Life'}, {'id': 72, 'name': 'Mathematics'}, {'id': 73, 'name': 'Natural'}, {'id': 74, 'name': 'Nature'}, {'id': 75, 'name': 'Physics'}, {'id': 76, 'name': 'Social'}, {'id': 77, 'name': 'Society'}, {'id': 78, 'name': 'Culture'}, {'id': 79, 'name': 'Documentary'}, {'id': 80, 'name': 'Personal'}, {'id': 81, 'name': 'Journals'}, {'id': 82, 'name': 'Philosophy'}, {'id': 83, 'name': 'Places'}, {'id': 84, 'name': 'Travel'}, {'id': 85, 'name': 'Relationships'}, {'id': 86, 'name': 'Sports'}, {'id': 87, 'name': 'Baseball'}, {'id': 88, 'name': 'Basketball'}, {'id': 89, 'name': 'Cricket'}, {'id': 90, 'name': 'Fantasy'}, {'id': 91, 'name': 'Football'}, {'id': 92, 'name': 'Golf'}, {'id': 93, 'name': 'Hockey'}, {'id': 94, 'name': 'Rugby'}, {'id': 95, 'name': 'Running'}, {'id': 96, 'name': 'Soccer'}, {'id': 97, 'name': 'Swimming'}, {'id': 98, 'name': 'Tennis'}, {'id': 99, 'name': 'Volleyball'}, {'id': 100, 'name': 'Wilderness'}, {'id': 101, 'name': 'Wrestling'}, {'id': 102, 'name': 'Technology'}, {'id': 103, 'name': 'True Crime'}, {'id': 104, 'name': 'TV'}, {'id': 105, 'name': 'Film'}, {'id': 106, 'name': 'After-Shows'}, {'id': 107, 'name': 'Reviews'}, {'id': 108, 'name': 'Climate'}, {'id': 109, 'name': 'Weather'}, {'id': 110, 'name': 'Tabletop'}, {'id': 111, 'name': 'Role-Playing'}, {'id': 112, 'name': 'Cryptocurrency'}], 'count': 112, 'description': 'Categories list.'}
catergories = payload['feeds']

cat_list = [] 

for catergory in catergories:
    # cat_list.append[catergory['name']]
    print(catergory)

print(cat_list)







