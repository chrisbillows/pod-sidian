from mvc_view import Display
from mvc_model import Model, DatabaseManager, Podcast
import time
import json
from typing import List, Dict, Any

from podcast_index_api import PodcastIndexConfig, PodcastIndexService


# ---------------------------------------------------------
#  MENU 0 - MAIN MENU
# ---------------------------------------------------------


class MainMenuHandler:
    """
    Handles the logic of displaying the menu to a user.

    Invalid inputs are handled within the class i.e. the "invalid" menu is not displayed
    through the controller but through the class itself.

    Otherwise displays the appropriate menu version, before return the appropriate 
    'next_menu' variable.
    """

    valid_choices = {
        "q": "main_menu_goodbye",
        "1": "view_tracked_podcasts_menu",
        "2": "stop_tracking_a_podcast_menu",
        "3": "download_history_menu",
        "4": "download_additional_episodes_menu",
        "5": "search_by_title_menu",
        "6": "trending_podcasts_menu",
        "7": "newly_launched_podcasts_menu",
        "8": "all_recent_episodes_menu",
        "9": "all_episodes_mentioning_a_person",
    }

    def __init__(self) -> None:
        self.display = Display()

    def main_menu(self, choice=None, max_attempts=None) -> str:
        """
        Displays full main menu once only. Get user choice and if it's invalid, keep 
        main menu displayed and display options reminder. 
        
        Args:
            choice( , optional):
            
            max_attempts( optional): The choice default allows for testing. The 
                max_attempts parameter is used to limit the number of iterations during 
                testing and avoid infinite loops.
        
        """
        full_menu_displayed = False
        attempts = 0

        while True:
            if max_attempts and attempts >= max_attempts: 
                return None

            if full_menu_displayed == False:
                self.display.main_menu_full()
                full_menu_displayed = True

            if not choice:  
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.main_menu_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 1 - VIEW TRACKED PODCASTS
# ---------------------------------------------------------


class ViewTrackedPodcastsHandler:
    valid_choices = {
        "d": "stop_tracking_a_podcast_menu",
        "m": "main_menu",
        "q": "main_menu_goodbye",
    }

    def __init__(self) -> None:
        self.display = Display()
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.idx_tracked_pods = list(enumerate(self.tracked_pods, 1))
        self.valid_indexes = len(self.tracked_pods)

    def tracked_pods_handler(self, choice=None, max_attempts=None) -> str:
        """
        Checks if tracked podcasts is an empty list. If not, displays tracked podcasts 
        and
        
        Args:

        
        
        """
        if self._tracked_pods_empty():
            self.display.view_tracked_podcasts_empty()
            next_menu = "main_menu"
            return next_menu

        attempts = 0
        full_menu_displayed = False

        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            if full_menu_displayed == False:
                self.display.view_tracked_podcasts_full(self.idx_tracked_pods)
                full_menu_displayed = True

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.view_tracked_podcasts_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

    def _tracked_pods_empty(self) -> bool:
        if self.valid_indexes == 0:
            return True


# ---------------------------------------------------------
#           MENU 2 - STOP TRACKING A PODCAST
# ---------------------------------------------------------


class StopTrackingPodcastHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.idx_tracked_pods = list(enumerate(self.tracked_pods, 1))
        self.valid_indexes = len(self.tracked_pods)
    
    # TODO supplanting this, lets add active/inactive status for deletion func.
    #       We have to add a lot more for the transcription stuff anyway
    #       And when it comes to keeping the transcript side in sync this will be
    #       very helpful.     

    # TODO currently displays list and returns to main menu after any key enter.
    # TODO deletion functionality needs to come from list_manager.py and be rewritten
    # TODO QUESTION is how we are handling valid index choices - for both checking and 
    #   especially for returning menu options
    # TODO e.g. we can't do next_menu = self.valid_choices[choice] because 1-x 
    #     aren't there - 1-x need to trigger the podcast deletion loops
    # TODO although I think that is pretty easy to add

    def stop_tracking_podcast_handler(self, choice=None, max_attempts=None) -> str:
        attempts = 0
        full_menu_displayed = False

        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            if full_menu_displayed == False:
                self.display.stop_tracking_a_podcast_full(
                    self.idx_tracked_pods, self.valid_indexes
                )
                full_menu_displayed = True

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.stop_tracking_a_podcast_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

    def _remove_tracked_podcast():
        pass


# ---------------------------------------------------------
#  MENU 3 - DOWNLOAD HISTORY
# ---------------------------------------------------------


class DownloadHistoryHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def download_history_handler(self, choice=None, max_attempts=None) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.download_history_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.download_history_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 4 - DOWNLOAD ADDITIONAL EPISODES
# ---------------------------------------------------------


class DownloadAdditionalsEpisodesHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def download_additional_episodes_handler(
        self, choice=None, max_attempts=None
    ) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.download_additional_episodes_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.download_additional_episodes_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 5 - SEARCH BY TITLE
# ---------------------------------------------------------


class SearchByTitleHandler:
    """
    Class to handle searching by title for the user.

    The class is structured around a sub-menu handler from which all other menus are 
    accessible, for maintaining flexibility for re-design.

    To consider is if some(all?) of these methods should be classes in their own right -
    depending on how complex movements between other catergories of menu need to be.  
    
    e.g. it might turn out to be logical to run searches from inside other deeply nested
    menus.  
    
    ALSO - when building the menus for episode downloader or podcast tracker, we might 
    find they are needed by many classes.  Will it make sense to end up with only one 
    class that has a sub menu handler?
    
    """
    valid_choices = {
        "m": "main_menu",
        "q": "main_menu_goodbye",
        "s": "_search_by_title_search_term_getter",
    }

    def __init__(self) -> None:
        self.display = Display()

    def search_by_title_sub_menu_handler(
        self,
    ) -> str:  # return a valid menu to the controller
        """
        Effectively the controller for this set of sub-menus.

        The order if menus is primary path through the menus; it is the order they would
        be called if they weren't structured in a while loop.
        
        The while loop continues to allow for ultimate flexibility in changing or 
        introducing user paths between menus.
        
        """
        next_sub_menu = "_search_by_title_search_term_getter"
        while True:
            if next_sub_menu == "_search_by_title_search_term_getter":
                next_sub_menu = self._search_by_title_search_term_getter()

            elif next_sub_menu == "_search_by_title_search_results_handler":
                next_sub_menu = self._search_by_title_search_results_handler()

            elif next_sub_menu == "_search_by_title_podcast_detail_handler":
                next_sub_menu = self._search_by_title_podcast_detail_handler()

            elif next_sub_menu == "main_menu":
                print("TEMP MSG: Sub-menu was triggered to main menu. Going there now")
                time.sleep(2)
                return "main_menu"

            elif next_sub_menu == "main_menu_goodbye":
                print("TEMP MSG: Sub-menu was triggered to goodbye. Going there now")
                time.sleep(2)
                return "main_menu_goodbye"

            else:
                print("TEMP MSG: Some kind of error has occured... returning to main menu")
                time.sleep(2)
                return "main_menu"

    def _search_by_title_search_term_getter(self) -> str:  # return a valid sub menu:
        """
        Display request to user for search term. Get the search term and checks if the 
        user is indicating they want a different menu. If so, the search term is reset.
        If not, the search term remains accessible to the class and the results 
        menu is selected.
                
        """
        self.display.search_by_title_enter_search_term()
        self.search_choice = input(": ")

        if self.search_choice in self.valid_choices.keys():
            next_sub_menu = self.valid_choices[self.search_choice]
            self.search_choice = ""
            return next_sub_menu  # this does return to main menu
        else:
            next_sub_menu = "_search_by_title_search_results_handler"
            return next_sub_menu

    def _search_by_title_search_results_handler(self) -> str:
        """
        Takes the search term and queries the API.
        
        Creates all required display variables, usable by the entire class.
        
        If the search result is empty - tells user and next_menu is 
        'empty_search_options'.
        
        If the search result is juicy, it display the search results.
        
        It takes a user choice, and checks its valid or another menu. If it's not, then 
        it creates an instance variable for the valid podcast choice and returns the 
        next required menu.
        
        """
        self.search_results = self._api_caller_get_search_results()
        self._generate_search_display_variables()

        if self._search_results_empty(self.search_results):
            self.display.search_by_title_results_empty(self.search_choice)
            self.search_choice = ''
            # no options for now, just bounce back into search
            next_sub_menu = "_search_by_title_search_term_getter"
            return next_sub_menu

        else:
            self.display.search_by_title_results(
                self.search_choice, self.idx_search_results, self.valid_indexes
            )

            while True:
                choice = input(": ")

                try:
                    choice_as_int = int(choice) 
                    if choice_as_int in self.valid_indexes_list:
                        self.selected_podcast = choice_as_int
                        next_sub_menu = "_search_by_title_podcast_detail_handler"
                        return next_sub_menu
                except (
                    ValueError
                ):  # if choice cannot convert to an int, do nothing and 
                    # proceed to next block
                    pass

                if choice in self.valid_choices:
                    next_menu = self.valid_choices[choice]
                    return next_menu

                else:
                    self.display.search_by_title_invalid()

    def _search_by_title_podcast_detail_handler(self):
        """
        Once a user has selected a podcast from the search results - this displays a 
        detailed view of the information.

        It also calls the class method to get episodes for the podcast, which it stores 
        as an instance variable to be available for further use (for example by the 
        episode downloader).

        It then asks the users for their choice how to proceed - forking into two new 
        classes, the tracked podcasts and episode download functionalities.
        
        """
        pod_feed = self.idx_search_results[self.selected_podcast-1][1]
        pod_feed_id = pod_feed['id']
        pod_total_ep_count = pod_feed['episodeCount']
        
        pod_eps = self._api_caller_get_feed_episodes(pod_feed_id, pod_total_ep_count)
        self.selected_podcast = Podcast(pod_feed, pod_eps)
        
        self.display.search_by_title_display_selected_podcast_detail(
            self.selected_podcast)
        
        # TODO this displays the detail of the podcast. We need to: 
        #           a) get the episodes 
        #           b) give the options
        #                  which are 1) track the podcast 
        #                            2) download episodes 
        #                               (+ new search, main menu and secret quit)
        
        
                    
        # TODO episodes working - and it's getting them all.  
        # need to handle the displaying
        
        # TODO consider complexity of this class - way too high. But how to strip it 
        # out?  And refactor again before we actually finish some functionality?
        
        print()
        print("This is as far as we got! Returning to main menu.")
        print()
        time.sleep(5)
        return "main_menu"

    def _api_caller_get_search_results(self) -> dict:
        """
        Uses the class instance variable self.search_choice for the searchByTitle API 
        call.
        
        Also contains a commented out version to call a cached response for testing.
        
        Called by _search_by_title_search_results_handler method.
        
        """
        #! DUMMY API CALL
        # file_path = (
        # "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/"
        # "pod-sidian/cache/podcast_index_outputs/sample_set/"
        # "001_search.json"
        # )
        # with open(file_path, "r") as json_file:
        #     api_response = json.load(json_file)
        #     # api_response = []
        #! REAL API CALL
        config = PodcastIndexConfig()
        podcast_index_instance = PodcastIndexService(config.headers)

        api_response = podcast_index_instance.search(self.search_choice, fulltext=True)
        search_results = api_response["feeds"]

        return search_results


    def _api_caller_get_feed_episodes(self, feed_id, total_ep_count) -> dict:
        """
        Private method called by _search_by_title_podcast_detail_handler to get episodes
        for displaying in podcast detail. 
        
        """
                
        #! DUMMY API CALL
        
        #! REAL API CALL
        config = PodcastIndexConfig()
        podcast_index_instance = PodcastIndexService(config.headers)
        
        api_response = podcast_index_instance.episodes_by_feed_id(
            feed_id, max=total_ep_count, fulltext=True)
                    
        episodes = api_response["items"]

        return episodes

    def _search_results_empty(self, search_results: dict) -> bool:
        """
        Returns a bool to indicate if the search results for a query where empty.
        """

        if len(search_results) == 0:
            return True

    def _generate_search_display_variables(self) -> bool:
        """
        Uses the instance variable self.search_results and creates all required 
        display variables.
        
        E.g.
        - an index/enumerated version of the search results for displaying indexes
        - a total of the valid indexes for use in ranges like "pick 1 - {valid_indexes}"
        - valid indexes list, for use when checking a user selection is valid

        This is slightly risky - calling methods relying on these variables without 
        having called this method will throw errors.
        
        """
        self.idx_search_results = list(enumerate(self.search_results, 1))
        self.valid_indexes = len(self.search_results)
        self.valid_indexes_list = list(range(1, self.valid_indexes))
        return True


# ---------------------------------------------------------
#  MENU 6 - TRENDING PODCASTS
# ---------------------------------------------------------


class TrendingPodcastsHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def trending_podcasts_handler(self, choice=None, max_attempts=None) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.trending_podcasts_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.trending_podcasts_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 7 - NEWLY LAUNCHED PODCASTS
# ---------------------------------------------------------


class NewlyLaunchedPodcastsHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def newly_launched_podcasts_handler(self, choice=None, max_attempts=None) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.newly_launched_podcasts_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.newly_launched_podcasts_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 8 - ALL RECENT EPISODES
# ---------------------------------------------------------


class AllRecentEpisodesHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def all_recent_episodes_handler(self, choice=None, max_attempts=None) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.all_recent_episodes_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.all_recent_episodes_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


# ---------------------------------------------------------
#  MENU 9 - All EPISODES MENTIONING A PERSON
# ---------------------------------------------------------


class AllEpisodesMentioningAPersonHandler:
    valid_choices = {"m": "main_menu", "q": "main_menu_goodbye"}

    def __init__(self) -> None:
        self.display = Display()

    def all_episodes_mentioning_a_person_handler(
        self, choice=None, max_attempts=None
    ) -> str:
        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            self.display.all_episodes_mentioning_a_person_full()

            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.all_episodes_mentioning_a_person_invalid()
                choice = (
                    None  # reset choice to None for next iteration if it was invalid
                )

            attempts += 1


class Controller:

    """
    Main controller class to run the programme.  A while loop built around a next_menu 
    variable to allow easily allow any menu to lead to any other menu - maximum flexible
    for adding/changing/evovling the UX."
    
    """

    def __init__(self):
        self.model = Model()
        self.display = Display()

    def run(self):
        next_menu = "main_menu"
        while True:
            # MENU 0 - MAIN MENU
            if next_menu == "main_menu":
                handler = MainMenuHandler()
                next_menu = handler.main_menu()
                continue

            elif next_menu == "not_built_yet":
                print("Not built yet!")
                next_menu = "main_menu_goodbye"

            elif next_menu == "main_menu_goodbye":
                self.display.main_menu_goodbye()
                break

            # MENU 1 - VIEW TRACKED PODCASTS
            elif next_menu == "view_tracked_podcasts_menu":
                handler = ViewTrackedPodcastsHandler()
                next_menu = handler.tracked_pods_handler()

            # MENU 2 - STOP TRACKING A PODCAST
            elif next_menu == "stop_tracking_a_podcast_menu":
                handler = StopTrackingPodcastHandler()
                next_menu = handler.stop_tracking_podcast_handler()

            # MENU 3 - DOWNLOAD HISTORY
            elif next_menu == "download_history_menu":
                handler = DownloadHistoryHandler()
                next_menu = handler.download_history_handler()

            # MENU 4 - DOWNLOAD ADDITIONAL EPISODES
            elif next_menu == "download_additional_episodes_menu":
                handler = DownloadAdditionalsEpisodesHandler()
                next_menu = handler.download_additional_episodes_handler()

            # MENU 5 - SEARCH BY TITLE
            elif next_menu == "search_by_title_menu":
                handler = SearchByTitleHandler()
                next_menu = handler.search_by_title_sub_menu_handler()

            # MENU 6 - TRENDING PODCASTS
            elif next_menu == "trending_podcasts_menu":
                handler = TrendingPodcastsHandler()
                next_menu = handler.trending_podcasts_handler()

            # MENU 7 - NEWLY LAUNCHED PODCASTS
            elif next_menu == "newly_launched_podcasts_menu":
                handler = NewlyLaunchedPodcastsHandler()
                next_menu = handler.newly_launched_podcasts_handler()

            # MENU 8 - ALL RECENT EPISODES
            elif next_menu == "all_recent_episodes_menu":
                handler = AllRecentEpisodesHandler()
                next_menu = handler.all_recent_episodes_handler()

            # MENU 9 - ALL EPISODES MENTIONING A PERSON
            elif next_menu == "all_episodes_mentioning_a_person":
                handler = AllEpisodesMentioningAPersonHandler()
                next_menu = handler.all_episodes_mentioning_a_person_handler()
                
            else:
                print(
                    "The menu returned by that method is not handled by controller.run," 
                    "bozo!"
                )
                break


if __name__ == "__main__":
    controller = Controller()
    controller.run()
