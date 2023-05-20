from view import Display
from model import Model, DatabaseManager
import time

class MainMenuHandler:
    """
    Handles the logic of displaying the menu to a user.
    
    Invalid inputs are handled within the class i.e. the "invalid" menu is not displayed through the controller but 
    through the class itself.
    
    Otherwise displays the appropriate menu version, before return the appropriate 'next_menu' variable.
    """
    
    valid_choices = {'q':'main_menu_goodbye', 
                     '1':'viewing_tracked_pods', 
                     '2':'not_built_yet', 
                     '3':'not_built_yet', 
                     '4':'not_built_yet',
                     '5':'not_built_yet', 
                     '6':'not_built_yet', 
                     '7':'not_built_yet', 
                     '8':'not_built_yet', 
                     '9':'not_built_yet'}
        
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
                self.display.main_menu()
                full_menu_displayed = True
            
            if not choice:  # for testing
                choice = input(": ")
        
            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice]
                return next_menu
            else:
                self.display.main_menu_truncated_no_clear_console()
                choice = None  # reset choice to None for next iteration if it was invalid
        
            attempts += 1

       
class ViewTrackedPodcastsHandler:
    
    valid_choices = {'d':'stop_tracking_podcast_menu', 
                     'm':'main_menu'}
            
    def __init__(self) -> None:
        self.display = Display()
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.idx_tracked_pods = list(enumerate(self.tracked_pods))
        self.indexes = len(self.tracked_pods)
    
    def tracked_pods_handler(self, choice=None, max_attempts=None) -> str:
        """
        Checks if tracked podcasts is an empty list. If not, displays tracked podcasts and 
        """
        if self._tracked_pods_empty():
            self.display.viewing_tracked_pods_empty()
            next_menu = 'main_menu'
            return next_menu
                
        attempts = 0
        full_menu_displayed = False
        
        while True:
            if max_attempts and attempts >= max_attempts:  # for testing
                return None
        
            if full_menu_displayed == False:
                self.display.viewing_tracked_pods_menu(self.idx_tracked_pods)
                full_menu_displayed = True
            
            if not choice:  # for testing
                choice = input(": ")
 
            if choice in self.valid_choices:
                next_menu = self.valid_choices[choice] 
                return next_menu
            else:
                self.display.viewing_tracked_pods_invalid()
                choice = None  # reset choice to None for next iteration if it was invalid
         
    def _tracked_pods_empty(self) -> bool:
        if self.indexes == 0:
            return True
       

class StopTrackingPodcastHandler:
    
    def __init__(self) -> None:
        self.dm = DatabaseManager()
        self.db = self.dm.json_getter()
        self.tracked_pods = self.db["podcasts being tracked"]
        self.indexes = len(self.tracked_pods)
    
    # def _tracked_pods_valid_choice_maker(self):
    #     idx_tracked_pods = list(enumerate(self.tracked_pods, 1))
    #     valid_idx_nums = list(range(1, len(self.tracked_pods) + 1))
    #     valid_idx_strs = [str(num) for num in valid_idx_nums]
        

class Controller:
    def __init__(self):
        self.model = Model()
        self.display = Display()

    def run(self):
            next_menu = 'main_menu'
            while True:
                
                if next_menu == 'main_menu':
                    handler = MainMenuHandler()                               
                    next_menu = handler.main_menu()
                    continue
     
                elif next_menu == 'viewing_tracked_pods':
                    handler = ViewTrackedPodcastsHandler()
                    next_menu = handler.tracked_pods_handler()
                    
                elif next_menu == 'stop_tracking_podcast_menu':
                    # handler = 
                    # next menu = 
                         
                elif next_menu == 'not_built_yet':
                    print("Not built yet!")
                    next_menu = 'main_menu_goodbye'
                    
                elif next_menu == 'main_menu_goodbye':
                    self.display.main_menu_goodbye()
                    break
                    


if __name__ == "__main__":
    controller = Controller()
    controller.run()
          

