from view import Display
from model import Model, DatabaseManager
import time


# ---------------------------------------------------------
#  MENU 0 - MAIN MENU
# ---------------------------------------------------------


class MainMenuHandler:
    """
    Handles the logic of displaying the menu to a user.
    
    Invalid inputs are handled within the class i.e. the "invalid" menu is not displayed through the controller but 
    through the class itself.
    
    Otherwise displays the appropriate menu version, before return the appropriate 'next_menu' variable.
    """
    
    valid_choices = {'q':'main_menu_goodbye', 
                     '1':'view_tracked_podcasts_menu', 
                     '2':'stop_tracking_a_podcast_menu', 
                     '3':'download_history_menu', 
                     '4':'download_additional_episodes_menu',
                     '5':'search_by_title_menu', 
                     '6':'trending_podcasts_menu', 
                     '7':'newly_launched_podcasts_menu', 
                     '8':'all_recent_episodes_menu', 
                     '9':'all_episodes_mentioning_a_person'}
        
    def __init__(self) -> None:
        self.display = Display()

    def main_menu(self, choice=None, max_attempts=None) -> str:
        """
        Displays full main menu once only. Get user choice and if it's invalid, keep main menu displayed and display options reminder.
        The choice default allows for testing. The max_attempts parameter is used to limit the number of iterations during testing and avoid 
        infinite loops.
        """
        full_menu_displayed = False
        attempts = 0
        
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None
        
            if full_menu_displayed == False:
                self.display.main_menu_full()
                full_menu_displayed = True
            
            if not choice:  # for testing
                choice = input(": ")
        
            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.main_menu_invalid()
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1


# ---------------------------------------------------------
#  MENU 1 - VIEW TRACKED PODCASTS
# ---------------------------------------------------------

       
class ViewTrackedPodcastsHandler:
    
    valid_choices = {'d':'stop_tracking_a_podcast_menu', 
                     'm':'main_menu'}
            
    def __init__(self) -> None:
        self.display = Display()
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.idx_tracked_pods = list(enumerate(self.tracked_pods, 1))
        self.valid_indexes = len(self.tracked_pods)
    
    def tracked_pods_handler(self, choice=None, max_attempts=None) -> str:
        """
        Checks if tracked podcasts is an empty list. If not, displays tracked podcasts and 
        """
        if self._tracked_pods_empty():
            self.display.view_tracked_podcasts_empty()
            next_menu = 'main_menu'
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
                choice = None  # reset choice to None for next iteration if it was invalid
         
    def _tracked_pods_empty(self) -> bool:
        if self.valid_indexes == 0:
            return True

# ---------------------------------------------------------
#           MENU 2 - STOP TRACKING A PODCAST
# ---------------------------------------------------------
       
class StopTrackingPodcastHandler:
    
    valid_choices = {'m':'main_menu'}
        
    def __init__(self) -> None:
        self.display = Display()
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.idx_tracked_pods = list(enumerate(self.tracked_pods, 1))
        self.valid_indexes = len(self.tracked_pods)
    
    # TODO currently display lists and returns to main menu after any key enter.
    # TODO deletion functionality needs to come from list_manager.py and be rewritten
    # TODO QUESTION is how we are handling valid index choices - for both checking and especially for returning menu options
    # TODO e.g. we can't do next_menu = self.valid_choices[choice] because 1-x aren't there - 1-x need to trigger the podcast deletion loops
    # TODO although I think that is pretty easy to add (but will it impact pytest?)
    
    def stop_tracking_podcast_handler(self, choice=None, max_attempts=None) -> str:
    
        attempts = 0
        full_menu_displayed = False
        
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None

            if full_menu_displayed == False:
                self.display.stop_tracking_a_podcast_full(self.idx_tracked_pods, self.valid_indexes)
                full_menu_displayed = True
                
            if not choice:  # for testing
                choice = input(": ")

            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice] 
                return next_menu
            else:
                self.display.stop_tracking_a_podcast_invalid()
                choice = None  # reset choice to None for next iteration if it was invalid
   
    def _remove_tracked_podcast():
        pass    


# ---------------------------------------------------------
#  MENU 3 - DOWNLOAD HISTORY
# ---------------------------------------------------------

class DownloadHistoryHandler:

    valid_choices = {'m':'main_menu'}
        
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
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1

# ---------------------------------------------------------
#  MENU 4 - DOWNLOAD ADDITIONAL EPISODES
# ---------------------------------------------------------

class DownloadAdditionalsEpisodesHandler:
    
    valid_choices = {'m':'main_menu'}
        
    def __init__(self) -> None:
        self.display = Display()
    
    def download_additional_episodes_handler(self, choice=None, max_attempts=None) -> str:

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
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1

# ---------------------------------------------------------
#  MENU 5 - SEARCH BY TITLE
# ---------------------------------------------------------

class SearchByTitleHandler:
    
    valid_choices = {'m':'main_menu'}
        
    def __init__(self) -> None:
        self.display = Display()
   
    def search_by_title_handler(self, choice=None, max_attempts=None) -> str:

        attempts = 0
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None
        
            self.display.search_by_title_full()
                                    
            if not choice:  # for testing
                choice = input(": ")
        
            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.search_by_title_invalid()
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1
        

# ---------------------------------------------------------
#  MENU 6 - TRENDING PODCASTS
# ---------------------------------------------------------

class TrendingPodcastsHandler:

    valid_choices = {'m':'main_menu'}
        
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
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1

# ---------------------------------------------------------
#  MENU 7 - NEWLY LAUNCHED PODCASTS
# ---------------------------------------------------------

class NewlyLaunchedPodcastsHandler:

    valid_choices = {'m':'main_menu'}
        
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
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1
    
# ---------------------------------------------------------
#  MENU 8 - ALL RECENT EPISODES
# ---------------------------------------------------------

class AllRecentEpisodesHandler:

    valid_choices = {'m':'main_menu'}
        
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
                choice = None  # reset choice to None for next iteration if it was invalid
            
            attempts += 1
    
# ---------------------------------------------------------
#  MENU 9 - All EPISODES MENTIONING A PERSON
# ---------------------------------------------------------

class AllEpisodesMentioningAPersonHandler:
    
    valid_choices = {'m':'main_menu'}
        
    def __init__(self) -> None:
        self.display = Display()
    
    def all_episodes_mentioning_a_person_handler(self, choice=None, max_attempts=None) -> str:

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
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1        

class Controller:
    
    """
    Main controller class to run the programme.  A while loop built around a next_menu variable to allow easily allow
    any menu to lead to any other menu - for easily expanding 
    """
    
    
    def __init__(self):
        self.model = Model()
        self.display = Display()

    def run(self):
            next_menu = 'main_menu'
            while True:

                # MENU 0 - MAIN MENU
                if next_menu == 'main_menu':
                    handler = MainMenuHandler()                               
                    next_menu = handler.main_menu()
                    continue
     
                elif next_menu == 'not_built_yet':
                    print("Not built yet!")
                    next_menu = 'main_menu_goodbye'
                    
                elif next_menu == 'main_menu_goodbye':
                    self.display.main_menu_goodbye()
                    break
                
                # MENU 1 - VIEW TRACKED PODCASTS   
                elif next_menu == 'view_tracked_podcasts_menu':
                    handler = ViewTrackedPodcastsHandler()
                    next_menu = handler.tracked_pods_handler()
                
                # MENU 2 - STOP TRACKING A PODCAST
                elif next_menu == 'stop_tracking_a_podcast_menu':
                    handler = StopTrackingPodcastHandler()
                    next_menu = handler.stop_tracking_podcast_handler()
        
                # MENU 3 - DOWNLOAD HISTORY
                elif next_menu == 'download_history_menu': 
                    handler = DownloadHistoryHandler()
                    next_menu = handler.download_history_handler()
                
                # MENU 4 - DOWNLOAD ADDITIONAL EPISODES
                elif next_menu == 'download_additional_episodes_menu':
                    handler = DownloadAdditionalsEpisodesHandler()
                    next_menu = handler.download_additional_episodes_handler()
                
                # MENU 5 - SEARCH BY TITLE
                elif next_menu == 'search_by_title_menu':
                    handler = SearchByTitleHandler()
                    next_menu = handler.search_by_title_handler()
                
                # MENU 6 - TRENDING PODCASTS
                elif next_menu == 'trending_podcasts_menu':
                    handler = TrendingPodcastsHandler()
                    next_menu = handler.trending_podcasts_handler()
                
                # MENU 7 - NEWLY LAUNCHED PODCASTS
                elif next_menu == 'newly_launched_podcasts_menu':
                    handler = NewlyLaunchedPodcastsHandler()
                    next_menu = handler.newly_launched_podcasts_handler()
                
                # MENU 8 - ALL RECENT EPISODES
                elif next_menu == 'all_recent_episodes_menu':
                    handler = AllRecentEpisodesHandler()
                    next_menu = handler.all_recent_episodes_handler()
                
                # MENU 9 - ALL EPISODES MENTIONING A PERSON
                elif next_menu == 'all_episodes_mentioning_a_person':
                    handler = AllEpisodesMentioningAPersonHandler()
                    
                else:
                    print("The menu returned by that method is not handled by controller.run, bozo!")
                    break    


if __name__ == "__main__":
    controller = Controller()
    controller.run()
          

