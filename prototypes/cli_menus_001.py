
def validate(valid_choices, usr_choice):
    if usr_choice in valid_choices:
        return True 
    else:
        print(f">>> INVALID CHOICE. Please pick again from: {', '.join(str(x) for x in valid_choices)}")
        return False


def view_and_delete(my_tracked_podcasts):
    while True:
        print("-----VIEW AND DELETE-----\n")
        tracked_pods = len(my_tracked_podcasts)

        if tracked_pods == 0:
            print("\nYou don't have any saved podcasts!\Returning to main menu.")
            break        

        for idx, pod in enumerate(my_tracked_podcasts):
            print(f"{idx}. {pod['title'].upper()}",
                f"{24 * '-'}",
                f"Episodes downloaded: {pod['ep_dloads']}",
                f"Tracked from: {pod['tracked_from']}",
                f"Lastest episode: {pod['last_ep']}",
                f"Link: {pod['link']}","",
                sep='\n')
        
        valid_idxs = list(range(1, len(my_tracked_podcasts)+1))

        if len(valid_idxs) == 0:
        

        print("Enter 1 to {valid_indexes} to return to main menu\n")
        
        
        
        menus = {'q': 'quit' }

    

#print("Enter the podcast number to delete: \nConfirm by typing YES in CAPITALS: \n")
#view_and_delete(my_tracked_podcasts)


def main_menu():
    print("----------MAIN MENU----------\n1. View and delete tracked podcasts\n2. Search and add a new podcast\nq. Quit the program\n")
    
    menus = {'1': 'view_and_delete'  , '2': 'search_and_add', 'q': 'quit' }
    
    valid_choices = list(menus.keys())
    valid = False 
    
    while valid == False:
        user_choice = input(": ")
        valid = validate(valid_choices, user_choice)
    go_to_menu = menus[user_choice]
    return go_to_menu

main_menu()