import json
import os


class dummy_JSON_maker():
    
    '''
        Class to take a dictionary and dir/file name and save it to JSON. 
        For use in development.
    '''

    def __init__(self, dictionary, output_dir, file_name) -> None:
        self.dictionary = dictionary
        self.output_dir = output_dir
        self.file_name = file_name
   
    def create_JSON(self):
        os.makedirs(self.output_dir, exist_ok=True)

        file_number = 1
        while True:
            output_file = f"{file_number:03d}_{self.file_name}.json"
            existing_files = os.listdir(self.output_dir)

            file_exists = False
            for file in existing_files:
                if file.startswith(f"{file_number:03d}_"):
                    file_exists = True
                    break

            if not file_exists:
                break

            file_number += 1
     
        with open(os.path.join(self.output_dir, output_file), "w") as f:
            json.dump(self.dictionary, f, indent=4)

        print("JSON successfully created")


class JSON_updater():
    '''
        Abandoned in favour of an even more basic example.
    '''

    def __init__(self, JSON_path, API_data) -> None:
        self.JSON_path = JSON_path
        self.API_data = API_data

    def import_json(self):
        with open(self.JSON_path, "r") as f:
            self.pod_directory = json.load(f)
                            
    def extract_existing_episodes(self):
        self.saved_ep_dicts = self.pod_directory['key5']


    def extract_saved_episode_ids(self):
        self.saved_ep_ids = [episode['id'] for episode in self.saved_ep_dicts]
        
    def compare_episodes():
        pass
        
    def add_new_episodes():
        pass

    def save_new_json():
        pass


#! creting the JSON
# new_json = dummy_JSON_maker(my_dict, output_directory, file_name)
# new_json.create_JSON()


#####################
# POC FOR ONE PODCAST 
#####################


def one_pod_example():
    '''
        saved pods has one episode dict.
        The API output is dummeid with recent episode items.
        The for loop checks new episodes against a list of saved episodes.
        And appends the episode dict if the ep_id is not in the list. 
    '''
    
    
    # DICT
    # (This will be a json)
    saved_pods = {
        'title': 'pod 1',
        'pod_id': '001',
        'episodes': [
            {
                'name': 'ep33',
                'ep_id': '2045',
                'data': 'episode data'
            },
            {
                'name': 'ep34',
                'ep_id': '2588',
                'data': 'episode data'
            },
            {
                'name': 'ep35',
                'ep_id': '3022',
                'data': 'episode data'
            }    
        ]
    }

    saved_episode_ids = [episode['ep_id'] for episode in saved_pods['episodes']] 

    #LIST 
    recent_episodes_items = [
        {
            'name': 'ep33',
            'ep_id': '2045',
            'data': 'episode data'
        },
        {
            'name': 'ep34',
            'ep_id': '2588',
            'data': 'episode data'
        },
        {
            'name': 'ep35',
            'ep_id': '3022',
            'data': 'episode data'
        },
        {
            'name': 'ep36',
            'ep_id': '3456',
            'data': 'episode data'
        },
        {
            'name': 'ep37',
            'ep_id': '3888',
            'data': 'episode data'
        }
    ] 

    for episode in recent_episodes_items:
        if episode['ep_id'] not in saved_episode_ids:
            saved_pods['episodes'].append(episode)
            print(f"appended {episode['ep_id']}")

    print(saved_pods)

        
#####################
# POC FOR THREE PODCAST 
#####################

# API returns
feed_001 = [
        {
            'name': 'ep34',
            'ep_id': '2588',
            'data': 'episode data'
        },
        {
            'name': 'ep35',
            'ep_id': '3022',
            'data': 'episode data'
        },
        {
            'name': 'ep36',
            'ep_id': '3456',
            'data': 'episode data'
        },
        {
            'name': 'ep37',
            'ep_id': '3888',
            'data': 'episode data'
        }
    ] 

feed_011 = [
        {
            'name': 'ep04',
            'ep_id': '5955',
            'data': 'episode data'
        },
        {
            'name': 'ep05',
            'ep_id': '6001',
            'data': 'episode data'
        }
    ]

feed_184 = [
        {
            'name': 'ep111',
            'ep_id': '10201',
            'data': 'episode data'
        },
        {
            'name': 'ep112',
            'ep_id': '10888',
            'data': 'episode data'
        },
        {
            'name': 'ep113',
            'ep_id': '11233',
            'data': 'episode data'
        }
    ]


def fake_api_call(pod_id):
    var_name = f'feed_{pod_id}'
    return globals()[var_name]

def three_pod_example():
    '''
        Builds on one_pod_example.
        saved pods is not a dictionary - with a list of "podcast being tracked"
        Function iterates over podcasts in podcast being tracked list.
        Fake API call dummies the API call - returning a list of recent episodes.
        This is then compared to the contents as in one_pod_example.

        THIS IS THE FULL LOGIC WE NEED, WORKING ON TINY JSON FILES./

    '''

    # DICT (This will be a json)
    saved_pods = {
        "podcasts being tracked": [
            {
                'title': 'pod 1',
                'pod_id': '001',
                'episodes': [
                    {
                        'name': 'ep33',
                        'ep_id': '2045',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep34',
                        'ep_id': '2588',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep35',
                        'ep_id': '3022',
                        'data': 'episode data'
                    }
                ],
            },
            {
                'title': 'pod 2',
                'pod_id': '011',
                'episodes': [
                    {
                        'name': 'ep02',
                        'ep_id': '5655',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep03',
                        'ep_id': '5855',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep04',
                        'ep_id': '5955',
                        'data': 'episode data'
                    }    
                ]
            },
            {
                'title': 'pod 3',
                'pod_id': '184',
                'episodes': [
                    {
                        'name': 'ep111',
                        'ep_id': '10201',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep112',
                        'ep_id': '10888',
                        'data': 'episode data'
                    },
                    {
                        'name': 'ep113',
                        'ep_id': '11233',
                        'data': 'episode data'
                    }    
                ]
            }    
        ]
    }

    for podcast in saved_pods['podcasts being tracked']:
        pod_id = podcast['pod_id']
        print(podcast['title'], pod_id)
        print(f"Saved episodes before: {[episode['ep_id'] for episode in podcast['episodes']]}")
        print("------------")
        
        recent_episodes = fake_api_call(pod_id)
        saved_episode_ids = [episode["ep_id"] for episode in podcast["episodes"]]
        for recent_episode in recent_episodes:
            if recent_episode["ep_id"] not in saved_episode_ids:
                podcast["episodes"].append(recent_episode)
        print(f"Saved episodes after: {[episode['ep_id'] for episode in podcast['episodes']]}")
        print()
        print()

three_pod_example()