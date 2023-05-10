from ast import Dict
import os
import datetime
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup
import textwrap
from rich import print as rprint
from rich.console import Console
from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI

# TODO Everything needs reworking if we're passing this as a dict
# TODO It's not worth it right now

def delete_podcast_menu(usr_choice, idx_tracked_pods, tracked_pods_full):
    # print(f"User selected: {usr_choice}")
    # print(f"User selection type is {type(usr_choice)}")
    # usr_int = int(usr_choice)
    # print(f"Choice as an int is {usr_int}")
    # print(f"Choice as an int is {type(usr_int)}")
    # print(f"Index type is {type(idx_tracked_pods[0][0])}")
  
    for idx, podcast in idx_tracked_pods:
        if idx == int(usr_choice):
            delete_title = podcast['title']

    # print("Deletion is: ")
    # print(delete_title)

    for pod in tracked_pods_full['podcasts being tracked']:
        if pod['title'] == delete_title:
            print(f"\nAre you sure you want to delete {pod['title'].upper()}?")
            confirm = input("Enter 'yes' to confirm: ")
            if confirm != 'yes':
                print('Deletion cancelled. Returning to main menu...')
                return tracked_pods_full 
            
            tracked_pods_full['podcasts being tracked'].remove(pod)
            print(f"\nDELETED {delete_title}\n")
        
    # tracked_pods = [item for index, item in idx_tracked_pods]
    print("\n\nYour remaining tracked podcasts are:\n")
    print([pod['title'] for pod in tracked_pods_full['podcasts being tracked']])
    print("\nReturning to main menu...\n")
    return tracked_pods_full

def view_and_delete_menu(tracked_pods_full):

    #------ TESTING ------
    # tracked_pods = tracked_pods_full['podcasts being tracked'] # tracked_pods is a list
    # total_tracked_pods = len(tracked_pods)
    # # idx_tracked_pods = list(enumerate(tracked_pods, 1))  #! this feels risky with our MASTER DATA
    # valid_idx_nums = list(range(1, total_tracked_pods + 1))
    # valid_idx_strs = [str(num) for num in valid_idx_nums]
    # valid_idx_joined = ', '.join(str(x) for x in valid_idx_nums)
    # for idx, podcast in list(enumerate(tracked_pods, 1)):
    #     print(f"{idx}. {podcast['title'].upper()}",
    #     f"{24 * '-'}",
    #     f"Link: {podcast['link']}","",
    #     #f"Episodes downloaded: {pod['ep_dloads']}",
    #     # f"Tracked from: {pod['tracked_from']}",
    #     #f"Lastest podcast: {pod['last_ep']}",
    #     sep='\n')
    #     for podcast in podcast['episodes']:
    #         print(f"{podcast['datePublishedPretty']} - EP: {podcast['podcast']} - {podcast['title']}")
    #         print()
    #------   ------ ------

    displayed = 0
    while True:
        tracked_pods = tracked_pods_full['podcasts being tracked'] # tracked_pods is a list
        total_tracked_pods = len(tracked_pods)
        if total_tracked_pods == 0:
            print("\n>>> You don't have any saved podcasts!\n\nReturning to main menu...\n")
            break

        idx_tracked_pods = list(enumerate(tracked_pods, 1))

        valid_idx_nums = list(range(1, total_tracked_pods + 1))
        valid_idx_strs = [str(num) for num in valid_idx_nums]

        if total_tracked_pods <= 5:
            valid_idx_joined = ', '.join(valid_idx_strs[:-1]) + ' or ' + valid_idx_strs[-1]
        else:
            valid_idx_joined = f"{valid_idx_strs[0]} - {valid_idx_strs[-1]}"

        if displayed == 0:
            print("-----VIEWING TRACKED PODCASTS-----\n")
            for idx, pod in idx_tracked_pods:
                print(f"{idx}. {pod['title'].upper()}")
                print(f"{24 * '-'}")
                print(f"Link: {pod['link']}")
                # f"Tracked from: {pod['tracked_from']}",
                print("Tracked episodes: ")
                
                if 'episodes' in pod:  # Check if the 'episodes' key exists, temp fix for non-production - when created by the app, episodes will always exist.
                    for episode in pod['episodes']:
                        print(f"{episode['datePublishedPretty']} | EP: {episode['episode']} - {episode['title']}")
                else:
                    print("No episodes found.")
                print()
                                       
        displayed = 1
        print("Enter 'q' to return to main menu.")
        print(f"Or, to delete a podcast to delete select {valid_idx_joined}: ")
        usr_choice = input(": ")
        
        # if usr_choice == 'q':
        #     print("\nReturning to main menu...\n")
        #     return tracked_pods   
        # if usr_choice == 'd':
        #     usr_select = input(f"")
        #     if usr_select in valid_idx_strs:
        #         tracked_pods = delete_podcast_menu(usr_select, idx_tracked_pods)
        #         return tracked_pods
        #     else:
        #         print("\n>>> INVALID CHOICE\n")
        # else:
        #     print("\n>>> INVALID CHOICE\n")          
            
        if usr_choice in valid_idx_strs:
            tracked_pods_full = delete_podcast_menu(usr_choice, idx_tracked_pods, tracked_pods_full)
            return tracked_pods_full
        elif usr_choice == 'q':
            print("\nReturning to main menu...\n")
            return tracked_pods
        else:
            print("\n>>> INVALID CHOICE\n")

def convert_unix_time(time_unix, format):
    date_time = datetime.datetime.fromtimestamp(time_unix)
    if format == 'date':
        human_readable = date_time.strftime("%Y-%m-%d")
    if format == 'date&time':
        human_readable = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return human_readable

def search_by_title_menu(tracked_pods):
    config_instance = PodcastIndexConfig()
    api_instance = PodcastIndexAPI(config_instance.config)
    
    displayed = 0
    while True:
        usr_search = input("\nEnter a search term (or 'q' to return to main menu): ")
        if usr_search == 'q':
            break
        
        # file_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/pi_output_cache/sample_api_responses/001_search.json"
        # with open(file_path, 'r') as json_file:
        #     dummy_api_response = json.load(json_file)
        #     #dummy_api_response = []

        # print(f"\nDUMMY DATA | SEARCH TERM NOT USED - search term input was: {usr_search}")

        api_response = api_instance.index.search(usr_search)

        total_search_results = len(api_response['feeds'])
        if total_search_results == 0:
            print("\n>>> No results for that search. PLEASE TRY AGAIN!\n\n")
            continue
    
        idxed_search_results = list(enumerate(api_response["feeds"], 1))

        valid_idx_nums = list(range(1, total_search_results + 1))
        valid_idx_strs = [str(num) for num in valid_idx_nums]
        # valid_idx_joined = ', '.join(str(x) for x in valid_idx_nums)
        
        if displayed == 0:
            for idx, podcast in idxed_search_results:
                title = podcast["title"]
                shortened_title = title if len(title) <= 30 else title[:30] + "..."
                formatted_title = f"{shortened_title:<33}"
            
                most_recent_ep = convert_unix_time(podcast['newestItemPubdate'], 'date')
            
                formatted_link = f'\033]8;;{podcast["link"]}\007{podcast["link"]}\033]8;;\007'
            
                print(f"{idx:>2}. - {formatted_title} | {most_recent_ep} | {formatted_link} | {podcast['language']}")
            displayed += 1
       
        while True:
            print(f"\n--------SEARCH OPTIONS-------\nEnter 1 - {total_search_results} to track a podcast\nEnter 'r' to (r)etry a new search term\nEnter 'q' to (q)uit search and return to the main menu")
            usr_choice = input(": ")
            if usr_choice in valid_idx_strs:
                tracked_pods = add_podcast_menu(usr_choice, idxed_search_results, tracked_pods)
                return tracked_pods
            elif usr_choice == 'q':
                print("\nReturning to main menu...\n")
                return tracked_pods
            elif usr_choice == 'r':
                break
            else:
                print("\n>>> INVALID CHOICE\nPlease choose again")

        if usr_choice == 'r':
            continue

        return tracked_pods

def dummy_add_latest_episodes(feed_title, feed_id):
    
    # get recent episodes DUMMY
    file_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/pi_output_cache/episode_for_track_pod/001_talk_python_last_23.json"
    with open(file_path, 'r') as json_file:
        dummy_api_response = json.load(json_file)

    recent_episode_list = dummy_api_response['items']

    # get recent episodes from API (20?)
    

    # display recent episodes?
    print("\n-------------------")
    print(feed_title.upper())
    print("-------------------\n")

    for podcast in recent_episode_list:
        ep_num = podcast['podcast']
        ep_title = podcast['title']
        ep_date = podcast['datePublishedPretty']
        ep_duration_seconds = podcast['duration']

        # REMOVE HTML     
        #! Likely issues. Need to experiment with more feeds / live with some uglyiness
        #! WILL BE BETTER TO TEST WITH FULL DESCRIPTION ENDPOINTS
        description = podcast["description"]
        soup = BeautifulSoup(description, "html.parser")
        text = soup.get_text("")
        terminal_width = os.get_terminal_size().columns
        description_wrapped = "\n".join(textwrap.fill(line, width=terminal_width) for line in text.split("\n"))    

        # DISPLAY HTML
        #! Needs to cover all possibilities - doesn't work on Talk Python, will be worse elsewhere
        # description = podcast["description"]
        # description = description.replace("<br/>", "\n")
        # console = Console()
                
        # Format links as clickable
        formatted_ep_link = f'\033]8;;{podcast["link"]}\007{podcast["link"]}\033]8;;\007'
        formatted_ep_mp3 = f'\033]8;;{podcast["enclosureUrl"]}\007{podcast["enclosureUrl"]}\033]8;;\007'
        
        print(f"{ep_num} - {ep_title.upper()}")
        print("--------------------------------------")
        print(f"Release date:     {ep_date}")
        print(f"Duration:         {int(ep_duration_seconds/60)} mins")
        print(f"Episode Page:     {formatted_ep_link}")
        print(f"Download link:    {formatted_ep_mp3}\n")
        print(description_wrapped)
        # console.print(description, markup=True)
        print()


    # save episodes
        print("Download podcast mp3 options to follow")
        print()

    # print("To save any episodes now, enter the index number.")
    # print("Enter x to save one podcast")
    # print("Enter idx1, idx2, idx3 etc. to save multiple episodes")
    # print("Enter idx - idx to save a range")
    # usr_choice = input(": ")

    # process usr_choice


    # save required episodes


    return recent_episode_list

def add_podcast_menu(usr_choice, idxed_search_results, tracked_pods_full):
    # print(f"\n\n{'-'* 25}\nI am tracked pods: {tracked_pods} - and my type is {type(tracked_pods)}\n{'-'* 25}\n\n")
    print("\n--------ADDING POD MENU--------")
    for podcast in idxed_search_results:
        if podcast[0] == int(usr_choice):
            categories_to_str = lambda categories: ', '.join(f"{k} - {v}" for k, v in categories.items())
            print("Are you sure you want to add: \n")
            print(podcast[1]['title'].upper())
            print(podcast[1]['description'])
            print(f"\nFeed_ID: {podcast[1]['id']}")
            print(f"itunes_ID: {podcast[1]['itunesId']}")
            print(f"Link: {podcast[1]['link']} ")
            print(f"RSS: {podcast[1]['url']} ")
            print(f"Episodes: {podcast[1]['episodeCount']} ")
            print(f"Language: {podcast[1]['language']} ")
            print(f"Categories: {categories_to_str(podcast[1]['categories'])}")
            print(f"\nMost recent ep:   {convert_unix_time(podcast[1]['newestItemPubdate'], 'date&time')}")
            print(f"Last update time: {convert_unix_time(podcast[1]['lastUpdateTime'], 'date&time')}")
            print(f"Last crawl time:  {convert_unix_time(podcast[1]['lastCrawlTime'], 'date&time')}")
            print(f"Last Parse time:  {convert_unix_time(podcast[1]['lastParseTime'], 'date&time')}")
            print(f"Last Good http:   {convert_unix_time(podcast[1]['lastGoodHttpStatusTime'], 'date&time')}")
            print(f"Last Update Time  {convert_unix_time(podcast[1]['lastUpdateTime'], 'date&time')}")
            print(f"Crawl errors: {podcast[1]['crawlErrors']}")
            print(f"Parse errors: {podcast[1]['parseErrors']}")
            
            # print(f"\n\n{'-'* 25}\nI am tracked pods: {tracked_pods} - and my type is {type(tracked_pods)}\n{'-'* 25}\n\n")

            confirm = input("\nIf you want to track this podcast, enter 'yes' to confirm add: ")
            if confirm != 'yes':
                print('\nAdd podcast cancelled. Returning to main menu... (maybe one day returns to search results?)')
                return tracked_pods_full
            
            # TODO ADD LATEST EPISODES
            # recent_episodes = dummy_add_latest_episodes(feed_title, feed_id) 
            # feed_title = podcast[1]['title'] 
            # feed_id = podcast[1]['id']
            # print(f"The feed id is {feed_id}")
            
            #TODO ADD TRACK TIME
            # add {podsidian: [{tracked_time: time}]} - this format allows for adding more metadata later if I want
            
            tracked_pods_full["podcasts being tracked"].append(podcast[1])
            print("-----NEW TRACKED PODS-----")
            print([x['title'] for x in tracked_pods_full['podcasts being tracked']])
            
            return tracked_pods_full    

def dummy_search_by_title_menu(tracked_pods_full):
    # print(f"\n\n{'-'* 25}\nI am tracked pods: {tracked_pods} - and my type is {type(tracked_pods)}\n{'-'* 25}\n\n")
    displayed = 0
    while True:
        usr_search = input("\nEnter a search term (or 'q' to return to main menu): ")
        if usr_search == 'q':
            break
        
        file_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/pi_output_cache/sample_api_responses/001_search.json"
        with open(file_path, 'r') as json_file:
            dummy_api_response = json.load(json_file)
            #dummy_api_response = []

        print(f"\nDUMMY DATA | SEARCH TERM NOT USED - search term input was: {usr_search}")
                
        total_search_results = len(dummy_api_response['feeds'])
        if total_search_results == 0:
            print("\n>>> No results for that search. PLEASE TRY AGAIN!\n\n")
            continue
    
        idxed_search_results = list(enumerate(dummy_api_response["feeds"], 1))

        valid_idx_nums = list(range(1, total_search_results + 1))
        valid_idx_strs = [str(num) for num in valid_idx_nums]
        # valid_idx_joined = ', '.join(str(x) for x in valid_idx_nums)
        
        if displayed == 0:
            for idx, podcast in idxed_search_results:
                title = podcast["title"]
                shortened_title = title if len(title) <= 30 else title[:30] + "..."
                formatted_title = f"{shortened_title:<33}"
            
                most_recent_ep = convert_unix_time(podcast['newestItemPubdate'], 'date')
            
                formatted_link = f'\033]8;;{podcast["link"]}\007{podcast["link"]}\033]8;;\007'
            
                print(f"{idx:>2}. - {formatted_title} | {most_recent_ep} | {formatted_link} | {podcast['language']}")
            displayed += 1
       
        while True:
            print(f"\n--------SEARCH OPTIONS-------\nEnter 1 - {total_search_results} to track a podcast\nEnter 'r' to (r)etry a new search term\nEnter 'q' to (q)uit search and return to the main menu")
            usr_choice = input(": ")
            if usr_choice in valid_idx_strs:
                tracked_pods_full = add_podcast_menu(usr_choice, idxed_search_results, tracked_pods_full)
                return tracked_pods_full
            elif usr_choice == 'q':
                print("\nReturning to main menu...\n")
                return tracked_pods_full
            elif usr_choice == 'r':
                break
            else:
                print("\n>>> INVALID CHOICE\nPlease choose again")

        if usr_choice == 'r':
            continue

        return tracked_pods_full

def search_and_add_menu(tracked_pods_full):
    while True:
        usr_option = input("\n-----SEARCH AND ADD MENU-----\n1. Search by title & author\n2. Other search\nq. Return to main menu\n: ")
        if usr_option == '1':
            tracked_pods = dummy_search_by_title_menu(tracked_pods_full)
            # tracked_pods = search_by_title_menu(tracked_pods)
            return tracked_pods    
        elif usr_option == '2':
            print("Not built yet")
            return tracked_pods
        else:
            break

def main_menu(tracked_pods_full: Dict):
    while True:
        valid_choices = ['1', '2', 'q']
        print("----------MAIN MENU----------\n1. View and delete tracked podcasts\n2. Search and add a new podcast\nq. Quit the program")
        usr_option = input(": ")
        if usr_option == '1':
            tracked_pods = view_and_delete_menu(tracked_pods_full)
        elif usr_option == '2':
            tracked_pods = search_and_add_menu(tracked_pods_full)
        elif usr_option == 'q':
            print("Thank you for using the programme. Goodbye!")
            break
        else:
            (f">>> INVALID CHOICE: Please pick again from: {', '.join(str(x) for x in valid_choices)}")
    print("---END---")  


# tracked_pods3 = {
#         "podcasts being tracked": 
#         [
#     ]
# }
# tracked_pods2 = []
# tracked_pods = [
# {'title': 'The Rest is History','ep_dloads': 3, 'tracked_from': '11/04/23', 
#  'link': 'https://shows.acast.com/the-rest-is-history-podcast', 'last_ep': '23/04/23 - "Atlantis"'},

# {'title': 'The Rest is Politics','ep_dloads': 28, 'tracked_from': '11/10/22', 
# 'link': 'https://shows.acast.com/the-rest-is-poltics-podcast', 
#  'last_ep': '23/04/23 - "Macron, Xi Jinping and striking teachers"'}
# ]

tracked_pods_json = 'tracked_pods_jsons/002_pods_from_json.json'

with open(tracked_pods_json, 'r') as f:
    json_data = f.read()
    tracked_pods_full = json.loads(json_data)

main_menu(tracked_pods_full)


