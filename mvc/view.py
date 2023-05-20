import os
import platform
import time

class Display:
    
    def __init__(self) -> None:
        pass
        
    def main_menu(self):
        self._clear_console()
        print("---------MAIN MENU--------")
        print()
        print("TRACKED PODCASTS")
        print("----------------")
        print("1. View tracked podcasts")
        print("2. Stop tracking a podcast")
        print("3. View episode download log")
        print("4. Download extra episodes")
        print()
        print("PODCAST SEARCH")
        print("--------------")
        print("5. Search by title")
        print("6. Trending podcasts (& by catergory)")
        print("7. New podcasts")
        print()
        print("EPISODE SEARCH")
        print("--------------")
        print("8. Search by person")
        print("9. Recent episodes (& by category)")
        print()
        print("Please select an option (1-9) or press 'q' to (q)uit")
        
    def main_menu_truncated_no_clear_console(self):
        print()
        print(">>> INVALID CHOICE")
        print()
        print("Please select 1 - 9 (or 'q' to quit the program)")
    
    def main_menu_goodbye(self):
        print()
        print("Thanks for using the program. Goodbye!")            
        print()
    
    def viewing_tracked_pods_menu(self, idx_tracked_pods):
        print("-----VIEWING TRACKED PODCASTS-----")
        print()
        for idx, pod in idx_tracked_pods:
            print(f"{idx}. {pod['title'].upper()}")
            print(f"{24 * '-'}")
            print(f"Link: {pod['link']}")
            # f"Tracked from: {pod['tracked_from']}",
            print("Last ten episodes: ")
            
            for episode in pod['episodes'][:10]:
                print(f"{episode['datePublishedPretty']} | EP: {episode['episode']} - {episode['title']}")
            print()
        print("Enter 'm' to return to (m)ain menu")
        print("Or, 'd' to select a podcast for deletion")
        
    # def viewing_tracked_podcasts_truncated():                           
    #     print("Enter 'q' to return to main menu.")
    #     print(f"Or, to delete a podcast to delete select {valid_idx_joined}: ")
    #     usr_choice = input(": ")
   
 
    def viewing_tracked_pods_empty(self):
        self._clear_console()
        print("-----VIEWING TRACKED PODCASTS-----")
        print()
        print("You don't have any saved podcasts!")
        print()
        print("Returning to main menu...")
        print()
        time.sleep(3)
    
    def viewing_tracked_pods_invalid(self):
        print(">>> INVALID CHOICE")
        print()
        print("Please select 'd' or 'm' ")
        
    def return_to_main(self):
        print()
        print("Returning to main menu...")
    
    def m1_del_conf(self):
        print("Are you sure you want to delete {PODCAST}")
        input("Enter'yes' to confirm: ")
        
    def m1_del_cancel(self):
        print("Deletion cancelled. Returning to main menu...")
    
    def m1_del_conf(self):
        print("Podcast deleted ")
                
    def m1_view_del_short(self):
        print("Enter 'q' to return to main menu.")
        print("Or, to delete a podcast to delete select 1, 2 or 3: ")
        input(": ")
        

    def _clear_console(self):
        if platform.system().lower() == "windows":
            os.system("cls")
        else:
            os.system("clear") 
        
