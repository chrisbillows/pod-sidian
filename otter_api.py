import requests
import base64
from http.cookies import SimpleCookie
import os
import json

API_BASE_URL = "https://otter.ai/forward/api/v1"
CSRF_COOKIE_NAME = "csrftoken"


def save_output_to_json(payload, method, output_directory):
    output_directory = output_directory
    os.makedirs(output_directory, exist_ok=True)

    file_number = 1
    while True:
        output_file = f"{file_number:03d}_{method}.json"
        existing_files = os.listdir(output_directory)

        file_exists = False
        for file in existing_files:
            if file.startswith(f"{file_number:03d}_"):
                file_exists = True
                break

        if not file_exists:
            break

        file_number += 1

    with open(os.path.join(output_directory, output_file), "w") as f:
        json.dump(payload, f, indent=4)


class OtterApi:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.csrfToken = ""
        self.user = {}
        self.session = requests.Session()

    def login(self):
        if not self.email or not self.password:
            raise Exception(
                "Email and/or password were not given. Can't perform authentication to otter.ai"
            )

        csrf_response = self.session.get(f"{API_BASE_URL}/login_csrf")
        csrf_cookie = SimpleCookie(csrf_response.headers["set-cookie"])
        self.csrfToken = csrf_cookie[CSRF_COOKIE_NAME].value

        login_response = self.session.get(
            f"{API_BASE_URL}/login",
            params={"username": self.email},
            headers={
                "authorization": f'Basic {base64.b64encode(f"{self.email}:{self.password}".encode()).decode()}',
                "x-csrftoken": self.csrfToken,
            },
        )

        self.user = login_response.json()["user"]

        print("Successfully logged in to Otter.ai")

        return login_response

    def get_speeches(self):
        response = self.session.get(
            f"{API_BASE_URL}/speeches", params={"userid": self.user["id"]}
        )

        # check that status code is 200 (HTTP OK)
        if response.status_code != 200:
            print(f"Error: received status code {response.status_code}")
            return None

        # check that response is not empty
        if not response.text:
            print("Error: received empty response")
            return None

        # try to parse response as JSON
        try:
            json_response = response.json()
        except ValueError as e:
            print(f"Error: could not parse response as JSON: {e}")
            return None

        with open(os.path.join("otter_api_outputs", "everything_001"), "w") as f:
            json.dump(json, f, indent=4)
            print("saved to json")

        return True  # json_response['speeches']

    # def get_speeches2(self, folder=0, page_size=45, source="owned"):
    #     # API URL
    #     speeches_url = OtterAI.API_BASE_URL + 'speeches'
    #     if self._is_userid_invalid():
    #         raise OtterAIException('userid is invalid')
    #     # Query Parameters
    #     payload = {'userid': self._userid,
    #             'folder': folder,
    #             'page_size': page_size,
    #             'source': source}
    #     # GET
    #     response = self._session.get(speeches_url, params=payload)

    #     return self._handle_response(response)

    def get_speech(self, speech_id):
        response = self.session.get(
            f"{API_BASE_URL}/speech",
            params={"speech_id": speech_id, "userid": self.user["id"]},
        )
        return response.json()["speech"]

    def speech_search(self, query):
        response = self.session.get(
            f"{API_BASE_URL}/speech_search",
            params={"query": query, "userid": self.user["id"]},
        )
        return response.json()["hits"]

    # The uploadSpeech function involves a multipart/form-data POST request,
    # which is out of scope for a brief example like this, but you would follow
    # a similar process to the above functions.


otter = OtterApi("christopherbillows@gmail.com", "3j_UhOs7vcQ")
otter.login()
speeches = otter.get_speeches()

print(speeches)
