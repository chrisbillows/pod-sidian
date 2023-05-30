import datetime
import hashlib
import json
import os
from typing import Any, Dict, Optional, Union
import warnings

import requests
from dotenv import load_dotenv


class OutputSaver:

    """
    A class to save Podcast Index API outputs.
    The root directory is "cache" and is not alterable.

    Attributes:
        output_main_dir (str): Main directory for output files. The full path will be
            "cache/output_main_dir". Default is "podcast_index_outputs".
        output_sub_dir (str): Subdirectory for output files. The full path will be
            "cache/output_main_dir/output_sub_dir". Default is "temp".

    Args:
        output_main_dir (str, optional): Main directory for output files. Defaults to
            "podcast_index_outputs".
        output_sub_dir (str, optional): Subdirectory for output files. Defaults to
        "temp".

    """

    def __init__(self, output_main_dir="podcast_index_outputs", output_sub_dir="temp"):
        self.output_main_dir = output_main_dir
        self.output_sub_dir = output_sub_dir

    def save_output_to_json(
        self,
        payload: Dict[str, Any],
        method_name: str,
        search_term: Optional[str] = None,
    ) -> None:
        file_number = 1
        while True:
            time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            if search_term:
                search_term = search_term.replace(" ", "-")
                output_file = (
                    f"{file_number:03d}_{method_name}_{search_term}_{time}.json"
                )
            else:
                output_file = f"{file_number:03d}_{method_name}_{time}.json"
            output_dir = os.path.join(
                "cache", self.output_main_dir, self.output_sub_dir
            )
            os.makedirs(output_dir, exist_ok=True)
            existing_files = os.listdir(output_dir)

            file_exists = False
            for file in existing_files:
                if file.startswith(f"{file_number:03d}_"):
                    file_exists = True
                    break

            if not file_exists:
                break

            file_number += 1

        with open(os.path.join(output_dir, output_file), "w") as f:
            json.dump(payload, f, indent=4)


class PodcastIndexConfig:

    """
    A class to create the required headers to access the Podcast Index API.

    The class uses environment variables to fetch API credentials and uses them to
    create the headers required for API requests.

    Attributes:
        api_key (str): API key retrieved from the environment variables.
        api_secret (str): API secret retrieved from the environment variables.
        headers (dict): The headers to be used for API requests, created using
            the API key and secret.

    """

    def __init__(self) -> None:
        self._load_environment_variables()
        self.api_key = os.getenv("podcast_index_api_key")
        self.api_secret = os.getenv("podcast_index_secret")
        self.headers = self._create_headers()

    @staticmethod
    def _load_environment_variables():
        load_dotenv()

    def _create_headers(self):
        epoch_time = int(datetime.datetime.now().timestamp())
        data_to_hash = self.api_key + self.api_secret + str(epoch_time)
        sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
        headers = {
            "X-Auth-Date": str(epoch_time),
            "X-Auth-Key": self.api_key,
            "Authorization": sha_1,
            "User-Agent": "Voyce",
        }
        return headers


class PodcastIndexService:

    """
    A class to handle API requests to Podcast Index endpoints.

    Class methods are organised in the same order as Podcast Index docs.
    Note that not all API available endpoints are covered.

    Attributes:
        headers (dict): A PodcastIndexConfig.headers instance variable.

    Args:
        headers (dict): The headers used for API requests.

    """

    def __init__(self, headers) -> None:
        self.headers = headers

    def search(self, query: str, max: int = None, fulltext: bool = False) -> dict:
        """
        Searches podcasts by term. Searched fields are title, owner and author.
        (Use search_by_title for a pure title search)

        The search can be customized with the optional `max` and `fulltext` parameters.

        Args:
            query (str): The term to search for.

            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                60. Defaults to None, in which case the API's default maximum is used.

            fulltext (bool, optional): Return the full text value of any text fields
                (ex: description). If not provided, text field values are truncated to
                100 words. If True, the string 'fulltext' is added to the payload.
                Defaults to False.

                Note the API requires a str 'fulltext' and not the bool used here.

        Returns:
            dict: The search results, in the form returned by the API.

        """

        # title, author or owner
        # docs state max = 1000 but I've been getting max = 60

        url = "https://api.podcastindex.org/api/1.0" + "/search/byterm"

        payload = {"q": query}

        if max is not None:
            payload["max"] = max

        if fulltext:
            payload[
                "fulltext"
            ] = "fulltext"  # in search_by_title this is changed to an actual bool

        response = self._make_request_get_result_helper(url, payload)

        return response

    def search_by_title(
        self, query: str, max: int = None, fulltext: bool = False, similar: bool = False
    ) -> dict:
        """
        Searches podcasts by term. Searched fields are title only.
        (Use search for title, owner and author).

        IN LIMITED TESTING THE SEARCH RESULTS WERE LESS USEFUL THAT 'search'. Use
        'search' for now.

        The search can be customized with the optional `max`, `fulltext` and `similar`
        parameters.

        Args:
            query (str): The term to search for.

            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                60. Defaults to None, in which case the API's default maximum is used.

            fulltext (bool, optional): Return the full text value of any text fields
                (ex: description). If not provided, text field values are truncated to
                100 words. If True, the string 'fulltext' is added to the payload.
                Defaults to False.

            similar (bool, optional): Return results for similar.  e.g. perhaps
                JavaScript for javascript. Available, although has made little
                difference in limited testing. Defaults to False.

        Returns:
            dict: The search results, in the form returned by the API.

        """

        warnings.warn(
            "The 'search_by_title' method utilise an endpoint that may be unreliable."
            " This method is therefore deprecated and may be removed in the future",
            DeprecationWarning,
        )

        url = "https://api.podcastindex.org/api/1.0" + "/search/bytitle"

        payload = {"q": query}

        if max is not None:
            payload["max"] = max

        if fulltext:
            payload[
                "fulltext"
            ] = True  # in search this requires the str 'fulltext', not a bool

        if similar:
            payload["similar"] = True

        response = self._make_request_get_result_helper(url, payload)

        return response

    def search_by_person(
        self, person: str, max: int = None, fulltext: bool = False
    ) -> dict:
        """
        Searches podcasts for a person. Searched fields are person tags, episode title,
        episode description, feed owner, feed author.

        The search can be customized with the optional `max` and `fulltext` parameters.

        Note also -  likeWon't work as an advanced search tool - seems to privilege
        title field. e.g. 'sandy hook' gets podcasts titled "Sandy etc" not where Sandy
        Hook is mentioned in the description.

        Args:
            person (str): The person to search for.

            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                100. Defaults to None, in which case the API's default maximum 60 is
                used.

            fulltext (bool, optional): Return the full text value of any text fields
                (ex: description). If not provided, text field values are truncated to
                100 words. If True, the string 'fulltext' is added to the payload.
                Defaults to False.

        Returns:
            dict: The search results, in the form returned by the API.

        """

        if max is not None and (max < 1 or max > 1000):
            raise ValueError("max must be between 1 and 1000")

        url = "https://api.podcastindex.org/api/1.0" + "/search/byperson"

        payload = {"q": person}

        if max is not None:
            payload["max"] = max

        if fulltext:
            payload["fulltext"] = True

        response = self._make_request_get_result_helper(url, payload)

        return response

    def podcast_by_feed_id(self, feed_id: int) -> dict:
        """
        Returns the podcast data aka feed data for a feed id.

        Can be used with recent_episodes aka 'recent/episodes' endpoint which returns
        episodes with feed_id but no feed information.

        Args:
            feed_id (int):  The podcast index feed id.

        """

        url = "https://api.podcastindex.org/api/1.0" + "/podcasts/byfeedid"

        payload = {"id": feed_id}

        response = self._make_request_get_result_helper(url, payload)

        return response

    def episodes_by_feed_id(
        self, feed_id: str, since: int = None, max: int = None, fulltext: bool = False
    ) -> dict:
        """
        Retrieves episodes by feed ID.

        The function queries the Podcast Index API's '/episodes/byfeedid' endpoint.
        The search can be customized with the optional `max`, `fulltext` and `similar`
        parameters.

        Args:
            feed_id (str): The feed ID to query for.

            since (int): Returns episode since the specified epoch timestamp.

            max (int, optional): The maximum number of episodes to return. The API
                documentation states a maximum of 1000, but in practice, this seems to
                vary.  Max I've seen is 330.
                Defaults to None, in which case the API's default maximum is used.

            fulltext (bool, optional): True returns the full text value of any text
                fields (ex: description). Otherwise text field values are truncated to
                100 words. Defaults to False.

        Returns:
            dict: The episodes by feed ID results, in the form returned by the API.
        """

        url = "https://api.podcastindex.org/api/1.0" + "/episodes/byfeedid"

        payload = {"id": feed_id}

        if max is not None:
            payload["max"] = max

        if since is not None:
            payload["since"] = since

        if fulltext:
            payload["fulltext"] = True

        response = self._make_request_get_result_helper(url, payload)

        return response

    def trending_podcasts(
        self,
        max: int = None,
        since: int = None,
        lang: str = None,
        cat: Union[str, int] = None,
        notcat: str = None,
    ) -> dict:
        """
        Returns the most recent podcasts considered "trending" by Podcast Index.  Seems
        to return in descending order of 'trendScore'

        Args:
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                XXX. Defaults to None, in which case the API's default maximum 10 is
                used.

            since (int, optional): Return items since the specified epoch timestamp.

            lang (str, optional): Specifying a language code (like "en") to return only
                episodes having that specific language. Multiple languages by accepted
                by separating them with commas. Also "unknown" accepted
                (ex. en,es,ja,unknown). Most common 'en' and 'en-us'.
                (Didn't see an endpoint to access all available languages.)

            cat (str or int, optional): Specify you ONLY want podcasts with these
            categories in the results. Separate multiple categories with commas. Accepts
            the category name or ID (or a mixture).

            notcat (str or int, optional): Specify to EXCLUDE podcasts with these
            categories in the results. Separate multiple categories with commas.
            Accepts the category name or ID (or a mixture).

        Returns:
            dict: The search results, in the form returned by the API.
        """

        url = "https://api.podcastindex.org/api/1.0" + "/podcasts/trending"
        # "https://api.podcastindex.org/api/1.0/podcasts/trending?max=10&since=1612125785&lang=en&cat=News&notcat=News"

        payload = {}

        if max is not None:
            payload["max"] = max

        if since is not None:
            payload["since"] = since

        if lang is not None:
            payload["lang"] = lang

        if cat is not None:
            payload["cat"] = cat

        if notcat is not None:
            payload["notcat"] = notcat

        response = self._make_request_get_result_helper(url, payload)

        return response

    def episode_by_episode_id(self, episode_id: int, fulltext: bool = False) -> dict:
        """
        Get an individual episode's data using the episode id. Episode IDs available
        from episodesByFeedID endpoint (and other end points).

        Args:
            episode_id (int): The podcast index id for the episode to download data for.

            fulltext (bool, optional): Return the full text value of any text fields
                (ex: description). If not provided, text field values are truncated to
                100 words. If True, the string 'fulltext' is added to the payload.
                Defaults to False.
        """
        url = "https://api.podcastindex.org/api/1.0" + "/episodes/byid"

        payload = {"id": episode_id}

        if fulltext:
            payload["fulltext"] = True

        response = self._make_request_get_result_helper(url, payload)

        return response

    # NUMBER 1 - ADDED EPISODES
    def recent_episodes(
        self,
        max: int = None,
        excludeString: str = None,
        before: int = None,
        fulltext: str = None,
    ) -> Dict:
        """
        Newest added episodes to Podcast Index's index, sorted from newest (it seems).

        NOT USED in favour of it's sibling function to "recent_feeds" which returns
        the FEEDS to which the newest episodes have been added.

        That endpoint is favoured for feed level field filtering e.g. lang, cat.

        Args:
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                XXX. Defaults to None, in which case the API's default maximum 40 is
                used.

            excludeString (str, optional): Excludes results where a specified exclude
            string appears in title or url fields.

            before (int, optional): Return items before the specified epoch timestamp.

            fulltext (bool, optional): Return the full text value of any text fields
                (ex: description). If not provided, text field values are truncated to
                100 words. If True, the string 'fulltext' is added to the payload.
                Defaults to False.

        """

        url = "https://api.podcastindex.org/api/1.0" + "/recent/episodes"

        payload = {}

        if max is not None:
            payload["max"] = max

        if excludeString is not None:
            payload["before"] = excludeString

        if before is not None:
            payload["since"] = before

        if fulltext is not None:
            payload["lang"] = fulltext

        response = self._make_request_get_result_helper(url, payload)

        return response

    # NUMBER 2 - FEEDS THAT HAVE HAD EPISODES ADDED TO THEM
    def recent_feeds(
        self,
        max: int = None,
        since: int = None,
        lang: str = None,
        cat: str = None,
        notcat: str = None,
    ) -> Dict:
        """
        Feeds with the newest added episodes, in reverse chronological order (per docs).

        This is used over similar recent_episodes endpoint, as it works as the feed
        level with lang, cat, and notcat filters.

        Args:
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                XXX. Defaults to None, in which case the API's default maximum 40 is
                used.

            since (int, optional): Return items since the specified epoch timestamp.

            lang (str, optional): Specifying a language code (like "en") to return only
                episodes having that specific language. Multiple languages by accepted
                by separating them with commas. Also "unknown" accepted
                (ex. en,es,ja,unknown). Most common 'en' and 'en-us'.
                (Didn't see an endpoint to access all available languages.)

            cat (str or int, optional): Specify you ONLY want podcasts with these
            categories in the results. Separate multiple categories with commas. Accepts
            the category name or ID (or a mixture).

            notcat (str or int, optional): Specify to EXCLUDE podcasts with these
            categories in the results. Separate multiple categories with commas.
            Accepts the category name or ID (or a mixture).
        """

        url = "https://api.podcastindex.org/api/1.0" + "/recent/feeds"

        payload = {}

        if max is not None:
            payload["max"] = max

        if since is not None:
            payload["since"] = since

        if lang is not None:
            payload["lang"] = lang

        if cat is not None:
            payload["cat"] = cat

        if notcat is not None:
            payload["cat"] = notcat

        response = self._make_request_get_result_helper(url, payload)

        return response

    # NUMBER 3 - NEWLY LAUNCHED/DISCOVERED FEEDS
    def recent_new_feeds(
        self, max: int = None, since: int = None, feedid: str = None, desc: bool = None
    ) -> Dict:
        """
        New podcasts added to Podcast Index in the last 24 hours.

        May be an eqivalent to recent_data. Limited ability to filter (language).
        Handled app side.

        Limited info returned - not even feed title. Will need to add feed by feedID
        endpoint and make multiple API calls to make the data useable in the app.

        Args:
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                XXX. Defaults to None, in which case the API's default maximum 40 is
                used.

            since (int, optional): Return items since the specified epoch timestamp.
        """

        url = "https://api.podcastindex.org/api/1.0" + "/recent/newfeeds"

        payload = {}

        if max is not None:
            payload["max"] = max

        if since is not None:
            payload["since"] = since

        if feedid is not None:
            payload["feedid"] = feedid

        if desc is not None:
            payload["desc"] = True

        response = self._make_request_get_result_helper(url, payload)

        return response

    # NUMBER 4 - ALSO NEWLY LAUNCHED/DISCOVERED FEEDS??
    def recent_data(self, max: int = None, since: int = None) -> Dict:
        """
        Docs suggest this mirrors functionality of recent/feeds - in testing seemed
        to mirror recent_new_feeds?

        Returns feeds ['feeds'] and episodes ['items'] - which seems to be the
        equivalent of the newly added feeds AND their newly added episodes?

        Returns more information per feed than

        Docs do state the 'recent/data' endpoint uses the date the feed was found by the
        index, rather than the feed's internal timestamp. That is available at
        'recent/newfeeds'.

        Args:
            max (int, optional): The maximum number of search results to return. The API
                documentation states a maximum of 1000, but in practice, it seems to be
                XXX. Defaults to None, in which case the API's default maximum XXX is
                used.

            since (int, optional): Return items since the specified epoch timestamp.
        """

        url = "https://api.podcastindex.org/api/1.0" + "/recent/data"

        payload = {}

        if max is not None:
            payload["max"] = max

        if since is not None:
            payload["since"] = since

        response = self._make_request_get_result_helper(url, payload)

        return response

    def categories(self):
        """
        Returns the categories used by Podcast Index. Categories can be used as
        parameters with some other endpoints.

        Returns:
            dict: The search results, in the form returned by the API.
        """
        url = "https://api.podcastindex.org/api/1.0" + "/categories/list"

        payload = {}

        response = self._make_request_get_result_helper(url, payload)

        return response

    # def multi_search_multi_endpoints(self, searches: list) -> bool:
    #     """
    #     DO NOT USE IN CURRENT STATE

    #     Half built placeholder function for testing endpoints:

    #     a) testing multiple search terms with a single API endpoint
    #     b) testing multiple search endpoints with the same search terms
    #     c) both

    #     Probably split into multi functions if ever required.

    #     """

    #     json_maker = OutputSaver()
    #     for search in searches:
    #         try:
    #             s_filename = search.replace(" ", "_")
    #             search_payload = self.search(s)
    #             search_by_title_payload = self.search_by_title(s)
    #             search_by_person_payload = self.search_by_person(search)
    #             json_maker.save_output_to_json(
    #                 search_by_person_payload,
    #                 method_name="search-by-person",
    #                 search_term=s_filename,
    #             )
    #         except Exception as e:
    #             print(f"Error occurred: {e}")
    #             return False
    #     return True

    def create_samples_of_all_api_calls(self):
        """
        Creates an example JSON for every api call in this PodcastIndexService class.

        Currently manual - add required instance methods to payloads with arguments to
        pass as tuples. (Remember the additional ',' required after single item tuples).

        Args:
            None

        There is a class below ValidQueriesExtractor - which creates a random list of
        automated valid criteria.  IT NEEDS UPDATING FROM THE PYTHON-PODCASTINDEX
        WRAPPER - it is a pointless time sink. DON'T DO IT!
        """

        payloads = {
            "search": ("True Crime", 500, True),
            "search_by_title": ("python",),
            "search_by_person": ("Guido van Rossum",),
            "podcast_by_feed_id": ("742305",),  # Talk Python to Me
            "episodes_by_feed_id": ("742305",),  # Talk Python to Me
            "trending_podcasts": ("",),
            "episode_by_episode_id": ("14187334485",),  # Real Python no. 149
            "recent_episodes": (),
            "recent_feeds": (),
            "recent_new_feeds": (),
            "recent_data": (),
            "categories": (),
        }

        json_maker = OutputSaver(output_sub_dir="sample_set")

        for method, values in payloads.items():
            payload = getattr(self, method)(*values)
            json_maker.save_output_to_json(payload, method)
        print("Sample API calls extracted")

        return True

    def _make_request_get_result_helper(self, url, payload):
        headers = self.headers
        result = requests.get(url, headers=headers, params=payload, timeout=5)
        result.raise_for_status()
        result_dict = json.loads(result.text)
        return result_dict


# class ValidQueriesExtractor:
#     """
#     THIS CODE WAS WRITTEN REFERENCING A DEPRECATED CLASS BUILT ON THE PYTHON-PODCAST
#     INDEX WRAPPER
#
#     IT NEEDS REWORKING COMPLETELY TO BE USEABLE. (AND SAVES VERY LITTLE TIME SO DO
#     NOT GET SUCKED INTO MESSING WITH IT!!!!)
#
#     A class to create a dictionary of valid queries (strings and ids) required for
#     each available API call in python-podcastindex.

#     For use by APICacher to create a cached JSON of each API call's output.

#     Extracts feed_id, itunes_id, and feed_url from a payload of trending podcasts,
#     returning the results from the first podcast with three valid outputs for those
#     fields.

#     It also extracts episode_id from a payload of recent episodes, returning the
#     result from the first episode with a valid output for
#     that field.

#     Three constants: SEARCH_TERM, SEARCH_PERSON and MAX complete the required query
#     variables for all the availble API calls.
#     """"

#     SEARCH_TERM = 'python'
#     SEARCH_PERSON = 'Guido van Rossum'
#     MAX = 10

#     def __init__(self, api_instance):
#         self.valid_queries = {'search_term': self.SEARCH_TERM,
#                               'person': self.SEARCH_PERSON,
#                               'max': self.MAX}
#         self.api_instance = api_instance

#     def get_all_valid_fields(self):
#         self.get_podcast_fields()
#         self.get_episode_field()
#         return self.valid_queries

#     def get_podcast_fields(self):
#         payload = self.api_instance.index.trendingPodcasts(10)

#         podcasts = payload['feeds']

#         for podcast in podcasts:
#             feed_id = podcast['id']
#             itunes_id = podcast['itunesId']
#             feed_url = podcast['url']

#             if self.is_valid_id(feed_id, itunes_id) and self.is_valid_url(feed_url):
#                 self.valid_queries.update (
#                                           {'feed_id': feed_id,
#                                            'itunes_id': itunes_id,
#                                            'feed_url': feed_url}
#                                            )
#                 return self.valid_queries
#         else:
#             return "No valid data"

#     def get_episode_field(self):
#         payload = self.api_instance.index.recentEpisodes(10)

#         episodes = payload['items']

#         for episode in episodes:
#             episode_id = episode['id']
#             if self.is_valid_id(episode_id):
#                 self.valid_queries['episode_id'] = episode_id
#                 return self.valid_queries
#         else:
#             return "No valid data"

#     def is_valid_id(self, *args):
#         for arg in args:
#             if not isinstance(arg, int) or arg is None:
#                 return False
#         return True

#     def is_valid_url(self, url):
#         url_pattern = re.compile(
#             r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
#         )
#         if not isinstance(url, str) or not url_pattern.match(url):
#             return False
#         else:
#             return True


# if __name__ == "__main__":

#     config = PodcastIndexConfig()
#     podcast_index_instance = PodcastIndexService(config.headers)
#     json_maker = OutputSaver()
