
def validate(valid_choices, usr_choice):
    if usr_choice in valid_choices:
        return True 
    else:
        print(f">>> INVALID CHOICE: Please pick again from: {', '.join(str(x) for x in valid_choices)}")
        return False

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
