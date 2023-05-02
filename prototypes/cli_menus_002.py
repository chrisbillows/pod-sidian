# list of tuples for now
import enum
from operator import index


tracked_pods2 = []
tracked_pods = [

{'title': 'The Rest is History','ep_dloads': 3, 'tracked_from': '11/04/23', 
 'link': 'https://shows.acast.com/the-rest-is-history-podcast', 'last_ep': '23/04/23 - "Atlantis"'},

{'title': 'The Rest is Politics','ep_dloads': 28, 'tracked_from': '11/10/22', 
'link': 'https://shows.acast.com/the-rest-is-poltics-podcast', 
 'last_ep': '23/04/23 - "Macron, Xi Jinping and striking teachers"'}
]


def main_menu(tracked_pods):
    while True:
        valid_choices = ['1', '2', 'q']
        usr_option = input("----------MAIN MENU----------\n1. View and delete tracked podcasts\n2. Search and add a new podcast\nq. Quit the program\n")
        if usr_option == '1':
            tracked_pods = view_and_delete_menu(tracked_pods)
        elif usr_option == '2':
            search_and_add_menu()
        elif usr_option == 'q':
            print("Thank you for using the programme. Goodbye!")
            break
        else:
            (f">>> INVALID CHOICE: Please pick again from: {', '.join(str(x) for x in valid_choices)}")
    print("---END---")  


# tracked_pods[0][0] = 1
# tracked_pods[0][1] = {dict}
# tracked_pods[0][1]['title'] = 'The Rest is History'

def delete_podcast_menu(usr_choice, idx_tracked_pods):
    # print(f"User selected: {usr_choice}")
    # print(f"User selection type is {type(usr_choice)}")
    # usr_int = int(usr_choice)
    # print(f"Choice as an int is {usr_int}")
    # print(f"Choice as an int is {type(usr_int)}")
    # print(f"Index type is {type(my_tracked_podcasts[0][0])}")
     
    for podcast in idx_tracked_pods:
        # only valid values should reach here
        if podcast[0] == int(usr_choice):
            print(f"\nAre you sure you want to delete {podcast[1]['title'].upper()}?")
            confirm = input("Enter 'yes' to confirm: ")
            if confirm != 'yes':
                print('Deletion cancelled. Returning to main menu...')
                tracked_pods = [item for index, item in idx_tracked_pods]
                return tracked_pods 
            
            idx_tracked_pods.remove(podcast)
            print(f"\nDELETED {podcast[1]['title']}\n")
            
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
        print(f"Please select podcast for deletion: {valid_idx_joined}\n(Or 'q' to return to main menu)")
        usr_choice = input(": ")
    
        if usr_choice in valid_idx_strs:
            tracked_pods = delete_podcast_menu(usr_choice, idx_tracked_pods)
            return tracked_pods
        elif usr_choice == 'q':
            print("\nReturning to main menu...\n")
            return tracked_pods
        else:
            print("\n>>> INVALID CHOICE\n")


def search_and_add_menu():
    while True:
        usr_option = input("\n---BYE---\n1. Print Goodbye\n2. Print FUCK OFF! \n3. Return to main menu\n: ")
        if usr_option == '1':
            print("Goodbye!")
            break
        elif usr_option == '2':
            print("FUCK OFF!")
            break
        else:
            break

main_menu(tracked_pods)


