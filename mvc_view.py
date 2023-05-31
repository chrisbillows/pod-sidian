from bs4 import BeautifulSoup
import datetime
import os
import platform
import time
from typing import Any, Dict
import re

from mvc_model import Podcast

class Display:
    def __init__(self) -> None:
        pass

    def _clear_console(self):
        if platform.system().lower() == "windows":
            os.system("cls")
        else:
            os.system("clear")

    def _display_unix_time(self, time_unix, format):
        date_time = datetime.datetime.fromtimestamp(time_unix)
        if format == "date":
            human_readable = date_time.strftime("%Y-%m-%d")
        if format == "date&time":
            human_readable = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return human_readable

    def _create_index_choice_sentence(self, valid_indexes):
        valid_idx_nums = list(range(1, valid_indexes + 1))
        valid_idx_strs = [str(num) for num in valid_idx_nums]

        if valid_indexes <= 5:
            valid_idx_joined = (
                ", ".join(valid_idx_strs[:-1]) + " or " + valid_idx_strs[-1]
            )
        else:
            valid_idx_joined = f"{valid_idx_strs[0]} - {valid_idx_strs[-1]}"
        return valid_idx_joined
    
    def _format_link(self, link: str) -> str:
        return f'\033]8;;{link}\007Link\033]8;;\007'
        
    def _format_html(self, html_string: str) -> str:
        
        # TODO More HTML variants we should tidy up? How many variants are possible?
        # Could this be a task I use a GPT API call for?  Give it the desired output
        # and let it output a best endeavours version?
        
        # print()
        # print("----HTML STRING---")
        # print(repr(html_string))
        # print()
        
        soup = BeautifulSoup(html_string, "html.parser")
        
        for br in soup.find_all("br"):
            br.replace_with("\n")

        for p in soup.find_all("p"):
            p.replace_with("\n" + p.get_text() + "\n")

        clean_text = soup.get_text()
        clean_text = clean_text.strip('\n')        
        clean_text = re.sub('\n+', '\n\n', clean_text)
        
        # print() 
        # print("----CLEAN STRING---")
        # print(repr(clean_text))
        # print()
        
        return clean_text
       
    # ---------------------------------------------------------
    #                   MENU 0 - MAIN MENU
    # ---------------------------------------------------------

    def main_menu_full(self):
        self._clear_console()
        print("---------MAIN MENU--------")
        #! THIS APPROACH IS IDEAL FOR WHEN I WANT TO MAKE THE HEADING USING TERMINAL WIDTH
        # def headline(text, border='-', width=50):
        #     return f" {text} ".center(width, border)
        print()
        print("TRACKED PODCASTS")
        print("----------------")
        print("1. View tracked podcasts")
        print("2. Stop tracking a podcast")
        print("3. Download history")
        print("4. Download additional episodes")
        print()
        print("PODCAST SEARCH")
        print("--------------")
        print("5. Search by title")
        print("6. Trending podcasts")
        print("7. Newly launched podcasts")
        print()
        print("EPISODE SEARCH")
        print("--------------")
        print("8. All recent episodes (from any podcast)")
        print("9. All episodes mentioning a person (from any podcast)")
        print()
        print("Please select an option (1-9) or press 'q' to (q)uit")

    def main_menu_invalid(self):
        print()
        print(">>> INVALID CHOICE")
        print()
        print("Please select 1 - 9 (or 'q' to (q)uit the program)")

    def main_menu_goodbye(self):
        print()
        print("Thanks for using the program. Goodbye!")
        print()

    # ---------------------------------------------------------
    #                   MENU 1 - VIEW TRACKED PODCASTS
    # ---------------------------------------------------------

    def view_tracked_podcasts_full(self, idx_tracked_pods):
        print("-----VIEWING TRACKED PODCASTS-----")
        print()
        for idx, pod in idx_tracked_pods:
            print(f"{idx}. {pod['title'].upper()}")
            print(f"{24 * '-'}")
            print(f"Link: {pod['link']}")
            # f"Tracked from: {pod['tracked_from']}",
            print()
            print("Last ten episodes: ")

            for episode in pod["episodes"][:10]:
                print(
                    f"{self._display_unix_time(episode['datePublished'], 'date')} | EP: {episode['episode']} - {episode['title']}"
                )
            print()
        print("Enter 'm' to return to (m)ain menu")
        print("Or, 'd' to select a podcast for (d)eletion")

    def view_tracked_podcasts_invalid(self):
        print()
        print(">>> INVALID CHOICE")
        print()
        print("Please select 'd' or 'm' ")

    def view_tracked_podcasts_empty(self):
        self._clear_console()
        print("-----VIEWING TRACKED PODCASTS-----")
        print()
        print("You don't have any saved podcasts!")
        print()
        print("Returning to main menu...")
        print()
        time.sleep(3)

    # ---------------------------------------------------------
    #                   MENU 2 - STOP TRACKING A PODCAST
    # ---------------------------------------------------------

    def stop_tracking_a_podcast_full(self, idx_tracked_pods, valid_indexes):
        print("-----STOP TRACKING A PODCAST-----")
        print()
        for idx, pod in idx_tracked_pods:
            print(f"{idx}. {pod['title'].upper()}")
        print()
        print(
            "To delete a podcast, select "
            f"{self._create_index_choice_sentence(valid_indexes)}: "
            "NOT BUILT YET"
        )
        print()
        print("Enter 'm' to return to main menu.")

    def stop_tracking_a_podcast_invalid(self):
        print()
        print(">>> INVALID CHOICE")
        print()
        print("Functionality not built yet. Only 'm' can free you!")

    def stop_tracking_a_podcast_user_confirmation(self):
        print("Are you sure you want to delete {PODCAST}")
        input("Enter'yes' to confirm: ")

    def stop_tracking_a_podcast_deletion_cancelled(self):
        print("Deletion cancelled. Returning to main menu...")

    def stop_tracking_a_podcast_deletion_successful(self):
        print("Podcast deleted ")

    # ---------------------------------------------------------
    #  MENU 3 - DOWNLOAD HISTORY
    # ---------------------------------------------------------

    def download_history_full(self):
        print()
        print("This will be the DOWNLOAD HISTORY OPTIONS")
        print()
        print("'m' to return to main menu")

    def download_history_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    # ---------------------------------------------------------
    #  MENU 4 - DOWNLOAD ADDITIONAL EPISODES
    # ---------------------------------------------------------

    def download_additional_episodes_full(self):
        print()
        print("This will be DOWNLOAD ADDITIONAL EPISODES")
        print()
        print("'m' to return to main menu")

    def download_additional_episodes_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    # ---------------------------------------------------------
    #  MENU 5 - SEARCH BY TITLE
    # ---------------------------------------------------------

    def search_by_title_enter_search_term(self):
        self._clear_console()
        print("---------SEARCH PODCASTS BY TITLE--------")
        print()
        print("Enter a search term (or 'm' to return to (m)ain menu): ")
        print()

    def search_by_title_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    def search_by_title_results(
        self, search_term: str, idx_search_results: dict, valid_indexes: int
    ) -> None:
        self._clear_console()
        print("---------SEARCH PODCASTS BY TITLE--------")
        print()
        for idx, podcast in idx_search_results:
            title = podcast["title"]
            shortened_title = title if len(title) <= 30 else title[:30] + "..."
            formatted_title = f"{shortened_title:<33}"
            most_recent_ep = self._display_unix_time(podcast["newestItemPubdate"], "date")
            formatted_link = self._format_link(podcast["link"])
            print(f"{idx:>2}. - {formatted_title} | {most_recent_ep} | {podcast['language']:>5} | {formatted_link}")
        print()
        print(f"Your search for {search_term} returned {valid_indexes} results")
        print()
        print(f"Enter 1 - {valid_indexes} to view more detail, to track the podcast and download episodes")
        print("Enter 's' to try a new (s)earch term")
        print("Enter 'm' to return to the (m)ain menu")

    def search_by_title_results_empty(self, search_term):
        self._clear_console()
        print("---------SEARCH PODCASTS BY TITLE--------")
        print()
        print("Oh no!")
        print(f'Your search for "{search_term}" returned no results.')
        print()
        print("Please try again")
        print()
        print("Returning to search menu in 3 seconds...")  
        time.sleep(3)

    def search_by_title_display_selected_podcast_detail(
        self,
        selected_podcast: Podcast
        ):
        print("--------SELECTED PODCAST DETAILS--------")
        print()
        print(selected_podcast.title.upper())
        print()
        print(self._format_html(selected_podcast.description))
        print()
        print(f"Feed_ID:         {selected_podcast.feed_id}")
        print(f"itunes_ID:       {selected_podcast.itunes_id}")
        print(f"Link:            {self._format_link(selected_podcast.link_url)}")
        print(f"RSS:             {self._format_link(selected_podcast.rss_url)} ")
        print(f"Episode Count:   {selected_podcast.episodes_count} ")
        print(f"Language:        {selected_podcast.language} ")
        print(f"Categories:      {selected_podcast.catergories_str}")
        print()
        print(f"Most recent ep:  {self._display_unix_time(selected_podcast.newest_item_pub, 'date&time')}")
        print()
        print("----FEED HEALTH----")
        print(f"Last Update Time  {self._display_unix_time(selected_podcast.last_feed_update, 'date&time')}")
        print(f"Last crawl time:  {self._display_unix_time(selected_podcast.last_crawl, 'date&time')}")
        print(f"Last Parse time:  {self._display_unix_time(selected_podcast.last_parse, 'date&time')}")
        print(f"Last Good http:   {self._display_unix_time(selected_podcast.last_good, 'date&time')}")
        print()
        print(f"Crawl errors: {selected_podcast.crawl_errors}")
        print(f"Parse errors: {selected_podcast.parse_errors}")
        print()
        print("-----LAST 5 EPISODES SUMMARY-----")
        for episode in selected_podcast.episodes_raw_output[:5]:
            if episode['episode']:
                print(f"{self._display_unix_time(episode['datePublished'], 'date')} | #{episode['episode']} - {episode['title']} | {self._format_link(episode['link'])}")
            else:
                print(f"{self._display_unix_time(episode['datePublished'], 'date')} - {episode['title']} | {self._format_link(episode['link'])}")
       
                
    def search_by_title_last_five_episodes_detail(self, selected_podcast: Podcast) -> None:
        """
        Method to display the last five episodes in detail.
        
        Now using LAST 5 EPISODES SUMMARY directly in search_by_title_display_selected_podcast_detail
        
        # TODO May be useful for episode display - or maybe remove
        """
        print("-----LAST 5 EPISODES DETAIL-----")
        for episode in selected_podcast.episodes_raw_output[:5]:
            print()
            if episode['episode']:
                print(f"{self._display_unix_time(episode['datePublished'], 'date')} | #{episode['episode']} - {episode['title']} | {self._format_link(episode['link'])}")
            else:
                print(f"{self._display_unix_time(episode['datePublished'], 'date')} - {episode['title']} | {self._format_link(episode['link'])}")
            print()
            print(self._format_html(episode["description"]))
            print()
                
    # ---------------------------------------------------------
    #  MENU 6 - TRENDING PODCASTS
    # ---------------------------------------------------------

    def trending_podcasts_full(self):
        print()
        print("This will be the TRENDING PODCASTS")
        print()
        print("'m' to return to main menu")

    def trending_podcasts_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    # ---------------------------------------------------------
    #  MENU 7 - NEWLY LAUNCHED PODCASTS
    # ---------------------------------------------------------

    def newly_launched_podcasts_full(self):
        print()
        print("This will be NEWLY LAUNCHED PODCASTS")
        print()
        print("'m' to return to main menu")

    def newly_launched_podcasts_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    # ---------------------------------------------------------
    #  MENU 8 - ALL RECENT EPISODES
    # ---------------------------------------------------------

    def all_recent_episodes_full(self):
        print()
        print("This will be ALL RECENT EPISODES")
        print()
        print("'m' to return to main menu")

    def all_recent_episodes_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")

    # ---------------------------------------------------------
    #  MENU 9 - ALL EPISODES MENTIONING A PERSON
    # ---------------------------------------------------------

    def all_episodes_mentioning_a_person_full(self):
        print()
        print("This will be EPISODES MENTIONING A PERSON")
        print()
        print("'m' to return to main menu")

    def all_episodes_mentioning_a_person_invalid(self):
        print()
        print("This will be the invalid option")
        print()
        print("Only 'm' can free you")
