import os
import datetime
from dotenv import load_dotenv
import json
import podcastindex
from bs4 import BeautifulSoup
import textwrap
from rich import print as rprint
from rich.console import Console
from dev_tools.api_dev_tools import PodcastIndexConfig, PodcastIndexAPI

tracked_pods2 = []
tracked_pods = [

{'title': 'The Rest is History','ep_dloads': 3, 'tracked_from': '11/04/23', 
 'link': 'https://shows.acast.com/the-rest-is-history-episode', 'last_ep': '23/04/23 - "Atlantis"'},

{'title': 'The Rest is Politics','ep_dloads': 28, 'tracked_from': '11/10/22', 
'link': 'https://shows.acast.com/the-rest-is-poltics-episode', 
 'last_ep': '23/04/23 - "Macron, Xi Jinping and striking teachers"'}
]

def delete_podcast_menu(usr_choice, idx_tracked_pods):
    # print(f"User selected: {usr_choice}")
    # print(f"User selection type is {type(usr_choice)}")
    # usr_int = int(usr_choice)
    # print(f"Choice as an int is {usr_int}")
    # print(f"Choice as an int is {type(usr_int)}")
    # print(f"Index type is {type(my_tracked_podcasts[0][0])}")
     
    for episode in idx_tracked_pods:
        # only valid values should reach here
        if episode[0] == int(usr_choice):
            print(f"\nAre you sure you want to delete {episode[1]['title'].upper()}?")
            confirm = input("Enter 'yes' to confirm: ")
            if confirm != 'yes':
                print('Deletion cancelled. Returning to main menu...')
                tracked_pods = [item for index, item in idx_tracked_pods]
                return tracked_pods 
            
            idx_tracked_pods.remove(episode)
            print(f"\nDELETED {episode[1]['title']}\n")
            
            # remove indexes
            tracked_pods = [item for index, item in idx_tracked_pods]
            print("\n\nYour remaining tracked podcasts are:\n")
            print(tracked_pods)
    print("Returning to main menu...")
    return tracked_pods

def view_and_delete_menu(tracked_pods):
    displayed = 0
    while True:
        total_tracked_pods = len(tracked_pods)
        if total_tracked_pods == 0:
            print("\n>>> You don't have any saved podcasts!\n\nReturning to main menu...\n")
            break

        idx_tracked_pods = list(enumerate(tracked_pods, 1))
        valid_idx_nums = list(range(1, total_tracked_pods + 1))
        valid_idx_strs = [str(num) for num in valid_idx_nums]
        valid_idx_joined = ', '.join(str(x) for x in valid_idx_nums)

        if displayed == 0:
            print("-----VIEW AND DELETE-----\n")
            for idx, pod in idx_tracked_pods:
                print(f"{idx}. {pod['title'].upper()}",
                f"{24 * '-'}",
                f"Episodes downloaded: {pod['ep_dloads']}",
                f"Tracked from: {pod['tracked_from']}",
                f"Lastest episode: {pod['last_ep']}",
                f"Link: {pod['link']}","",
                sep='\n')
       
        displayed = 1
        print(f"Please select episode for deletion: {valid_idx_joined}\n(Or 'q' to return to main menu)")
        usr_choice = input(": ")
    
        if usr_choice in valid_idx_strs:
            tracked_pods = delete_podcast_menu(usr_choice, idx_tracked_pods)
            return tracked_pods
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
    # TO FINISH - building using dummy_search_by_title_menu
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

    for episode in recent_episode_list:
        ep_num = episode['episode']
        ep_title = episode['title']
        ep_date = episode['datePublishedPretty']
        ep_duration_seconds = episode['duration']

        # REMOVE HTML     
        #! Likely issues. Need to experiment with more feeds / live with some uglyiness
        #! WILL BE BETTER TO TEST WITH FULL DESCRIPTION ENDPOINTS
        description = episode["description"]
        soup = BeautifulSoup(description, "html.parser")
        text = soup.get_text("")
        terminal_width = os.get_terminal_size().columns
        description_wrapped = "\n".join(textwrap.fill(line, width=terminal_width) for line in text.split("\n"))    

        # DISPLAY HTML
        #! Needs to cover all possibilities - doesn't work on Talk Python, will be worse elsewhere
        # description = episode["description"]
        # description = description.replace("<br/>", "\n")
        # console = Console()
                
        # Format links as clickable
        formatted_ep_link = f'\033]8;;{episode["link"]}\007{episode["link"]}\033]8;;\007'
        formatted_ep_mp3 = f'\033]8;;{episode["enclosureUrl"]}\007{episode["enclosureUrl"]}\033]8;;\007'
        
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
    # print("To save any episodes now, enter the index number.")
    # print("Enter x to save one episode")
    # print("Enter idx1, idx2, idx3 etc. to save multiple episodes")
    # print("Enter idx - idx to save a range")
    # usr_choice = input(": ")

    # process usr_choice


    # save required episodes


    return recent_episode_list

def add_podcast_menu(usr_choice, idxed_search_results, tracked_pods):
    print("\n--------ADDING POD MENU--------")
    for episode in idxed_search_results:
        if episode[0] == int(usr_choice):
            categories_to_str = lambda categories: ', '.join(f"{k} - {v}" for k, v in categories.items())
            print("Are you sure you want to add: \n")
            print(episode[1]['title'].upper())
            print(episode[1]['description'])
            print(f"\nFeed_ID: {episode[1]['id']}")
            print(f"itunes_ID: {episode[1]['itunesId']}")
            print(f"Link: {episode[1]['link']} ")
            print(f"RSS: {episode[1]['url']} ")
            print(f"Episodes: {episode[1]['episodeCount']} ")
            print(f"Language: {episode[1]['language']} ")
            print(f"Categories: {categories_to_str(episode[1]['categories'])}")
            print(f"\nMost recent ep:   {convert_unix_time(episode[1]['newestItemPubdate'], 'date&time')}")
            print(f"Last update time: {convert_unix_time(episode[1]['lastUpdateTime'], 'date&time')}")
            print(f"Last crawl time:  {convert_unix_time(episode[1]['lastCrawlTime'], 'date&time')}")
            print(f"Last Parse time:  {convert_unix_time(episode[1]['lastParseTime'], 'date&time')}")
            print(f"Last Good http:   {convert_unix_time(episode[1]['lastGoodHttpStatusTime'], 'date&time')}")
            print(f"Last Update Time  {convert_unix_time(episode[1]['lastUpdateTime'], 'date&time')}")
            print(f"Crawl errors: {episode[1]['crawlErrors']}")
            print(f"Parse errors: {episode[1]['parseErrors']}")
            
            confirm = input("\nIf you want to track this podcast, enter 'yes' to confirm add: ")
            if confirm != 'yes':
                print('Add podcast cancelled. Returning to main menu... (maybe one day returns to search results?)')
                return tracked_pods 
            
            feed_title = episode[1]['title'] 
            feed_id = episode[1]['id']
            
            # print(f"The feed id is {feed_id}")
            dummy_add_latest_episodes(feed_title, feed_id) 
            
            tracked_pods.append(episode[1])
            # add {podsidian: [{tracked_time: time}]} - this format allows for adding more metadata later if I want
            print("-----NEW TRACKED PODS-----")
            for pod in tracked_pods:
                print(pod['title'])
            print(tracked_pods)

            return tracked_pods    

def dummy_search_by_title_menu(tracked_pods):
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
            for idx, episode in idxed_search_results:
                title = episode["title"]
                shortened_title = title if len(title) <= 30 else title[:30] + "..."
                formatted_title = f"{shortened_title:<33}"
            
                most_recent_ep = convert_unix_time(episode['newestItemPubdate'], 'date')
            
                formatted_link = f'\033]8;;{episode["link"]}\007{episode["link"]}\033]8;;\007'
            
                print(f"{idx:>2}. - {formatted_title} | {most_recent_ep} | {formatted_link} | {episode['language']}")
            displayed += 1
       
        while True:
            print(f"\n--------SEARCH OPTIONS-------\nEnter 1 - {total_search_results} to track a episode\nEnter 'r' to (r)etry a new search term\nEnter 'q' to (q)uit search and return to the main menu")
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

def search_and_add_menu(tracked_pods):
    while True:
        usr_option = input("\n-----SEARCH AND ADD MENU-----\n1. Search by title & author\n2. Other search\nq. Return to main menu\n: ")
        if usr_option == '1':
            tracked_pods = dummy_search_by_title_menu(tracked_pods)
            return tracked_pods    
        elif usr_option == '2':
            print("Not built yet")
            return tracked_pods
        else:
            break

def main_menu(tracked_pods):
    while True:
        valid_choices = ['1', '2', 'q']
        print("----------MAIN MENU----------\n1. View and delete tracked podcasts\n2. Search and add a new episode\nq. Quit the program")
        usr_option = input(": ")
        if usr_option == '1':
            tracked_pods = view_and_delete_menu(tracked_pods)
        elif usr_option == '2':
            tracked_pods = search_and_add_menu(tracked_pods)
        elif usr_option == 'q':
            print("Thank you for using the programme. Goodbye!")
            break
        else:
            (f">>> INVALID CHOICE: Please pick again from: {', '.join(str(x) for x in valid_choices)}")
    print("---END---")  

main_menu(tracked_pods)


