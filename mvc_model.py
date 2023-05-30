import os
from datetime import datetime
import json
from typing import List, Dict, Any


class Model:
    pass


class DatabaseManager:
    def __init__(self):
        self.tracked_pods_json_directory = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/LIVE_DATABASE"
        self.metafile_path = "/Users/chrisbillows/Documents/CODE/MY_GITHUB_REPOS/pod-sidian/LIVE_METAFILE/metafile.txt"

    def json_getter(self) -> Dict[str, Any]:
        """Facade to load the latest version of the tracked podcast into memory. Creates one if no file found."""
        self._ensure_json_directory_exists()
        no_current_json = self._check_if_dir_empty()
        if no_current_json:
            self._write_blank_json()  # also updates metafile
        current_tracked_json = self._load_latest_json()
        return current_tracked_json

    def json_writer(self, updated_current_tracked_json) -> None:
        """
        Takes a dictionary that will be a revised version of current_tracked_json. i.e. The function will have been passed current_tracked_json in
        memory and altered it.

        Alterations would be a) adding a podcast b) deleting a podcast c) adding tracked episodes.

        Function writes the updated version to LIVE_DATABASE with to a new file with an incremented file number {00n+1}.

        This will become the 'new' current_tracked_json the next time the database is checked.

        Previous versions of current_tracked_json are currently preserved.

        The function returns None.

        This is intentional. If a display of the updated current_tracked_json is required, this should be reloaded, to display to the user the
        database's current state.
        """
        self._ensure_json_directory_exists()
        no_current_json = self._check_if_dir_empty()
        if no_current_json:
            self._write_blank_json()  # also updates metafile

        file_number = len(self._list_files_in_LIVE_DATABASE()) + 1
        formatted_datetime = self._json_formatted_date()
        output_file = f"{file_number:04d}_TRACKED_PODS_{formatted_datetime}.json"
        updated_tracked_json = os.path.join(
            self.tracked_pods_json_directory, output_file
        )

        with open(updated_tracked_json, "w") as f:
            json.dump(updated_current_tracked_json, f, indent=4)

        self._update_metafile(updated_tracked_json)

    def _ensure_json_directory_exists(self) -> None:
        os.makedirs(self.tracked_pods_json_directory, exist_ok=True)

    def _check_if_dir_empty(self) -> bool:
        existing_files = self._list_files_in_LIVE_DATABASE()
        if len(existing_files) == 0:
            return True
        else:
            return False

    def _write_blank_json(self) -> None:
        """
        Called if check_dir_empty shows LIVE_DATABASE is empty. Saves a formatted blank podcast JSON to LIVE_DATABASE and updates the metafile.
        Does not load the JSON into memory or return anything.
        """
        tracked_pods_blank = {"podcasts being tracked": []}

        formatted_datetime = self._json_formatted_date()
        output_file = f"0001_TRACKED_PODS_{formatted_datetime}.json"
        updated_tracked_json = os.path.join(
            self.tracked_pods_json_directory, output_file
        )

        with open(updated_tracked_json, "w") as f:
            json.dump(tracked_pods_blank, f, indent=4)

        self._update_metafile(updated_tracked_json)

    def _load_latest_json(self) -> Dict[str, Any]:
        """
        Loads the latest version of tracked podcasts into memory, using the lastest version filename from the metafile.
        """
        latest_version = self._get_current_file_name()
        with open(latest_version, "r") as f:
            json_data = f.read()
            tracked_pods_full = json.loads(json_data)
        return tracked_pods_full

    def _list_files_in_LIVE_DATABASE(self) -> List[str]:
        """
        Returns a list of strings. Each string is the filename of a file in LIVE_DATABASE. Each file is a previous version of tracked pods.
        """
        existing_files = os.listdir(self.tracked_pods_json_directory)
        return existing_files

    def _update_metafile(self, latest_file_name: str) -> None:
        """
        Currently only called by `write_blank_json`. Updates the metafile with the filename for the latest tracked_pods JSON.
        """
        with open(self.metafile_path, "w") as metafile:
            metafile.write(latest_file_name)

    def _get_current_file_name(self) -> str:
        """
        Currenly called only by `load_latest_json`. Gets the name of the latest version of tracked podcasts from the metafile.
        """
        with open(self.metafile_path, "r") as metafile:
            latest_file_name = metafile.read().strip()
        return latest_file_name

    def _json_formatted_date(self) -> str:
        """
        Only called by `write_blank_json`. Creates a formatted now datetime for the file name of new tracked pods JSONs.
        """
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d %H%M")
        return formatted_datetime


# database_manager = DatabaseManager()
# latest_data = database_manager.json_getter()
# database_manager.json_writer()
