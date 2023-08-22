import json


class DramaDatabase:
    def __init__(self) -> None:
        self._database = []
        self._database_file = "drama-database.json"
        self._ids_cache = []

    @property
    def ids(self):
        if self._ids_cache:
            return self._ids_cache

        self._ids_cache = [
            int(entry.get("id")) for entry in self.database if entry.get("id", False)
        ]

        return self._ids_cache

    @property
    def database(self):
        """
        Property to lazily load and access the database content.
        """
        if not self._database:
            with open(self._database_file, "r") as database_file:
                self._database = json.load(database_file)
        return self._database

    def update(self, drama_id: int, new_data: dict) -> None:
        """
        Update a drama entry in the database with new data.

        Args:
            drama_id (int): The ID of the drama to be updated.
            new_data (dict): New data to update the drama entry with.
        """
        for entry in self._database:
            if entry.get("id") == drama_id:
                entry.update(new_data)
                self.save()
                break

    def save(self):
        """
        Save the current state of the database to the JSON file.

        This method writes the current content of the database to the associated JSON file,
        preserving any changes made to the data.

        Note:
            This method should be called after making modifications to the database.
        """

        sorted_database = sorted(self._database, key=lambda x: x["id"])
        with open(self._database_file, "w") as database_file:
            json.dump(sorted_database, database_file, separators=(",", ":"))

    def contains_id(self, id: int) -> bool:
        """
        Check if the database contains an entry with the given drama ID.

        Args:
            drama_id (int): The ID of the drama.

        Returns:
            bool: True if the drama ID is found, otherwise False.
        """
        return id in self.ids

    def add_drama(self, drama_info: dict) -> None:
        """
        Add a drama entry to the database.

        Args:
            drama_info (dict): Information about the drama to be added.
        """
        if not self._database:
            self._database = self.database

        synonyms = drama_info.get("alt_titles", [])

        if drama_info.get("original_title", False):
            synonyms = synonyms + list(drama_info.get("original_title", ""))

        tags = []
        if isinstance(drama_info.get("tags"), list):
            tags = drama_info.get("tags", [])

        genres = []
        if isinstance(drama_info.get("genres"), list):
            genres = drama_info.get("genres", [])

        tags = list(tags) + list(genres)

        drama_entry = {
            "id": drama_info.get("id", ""),
            "sources": drama_info.get("sources", []),
            "title": drama_info.get("title", ""),
            "type": drama_info.get("type", ""),
            "episodes": drama_info.get("episodes", ""),
            "status": drama_info.get("status", ""),
            "year": drama_info.get("year", ""),
            "picture": drama_info.get("images", {}).get("poster", ""),
            "thumbnail": drama_info.get("images", {}).get("thumb", ""),
            "synonyms": synonyms,
            "tags": tags,
        }

        self._ids_cache.append(drama_info.get("id"))
        self._database.append(drama_entry)

    def add_bulk_dramas(self, drama_list: list) -> None:
        """
        Add multiple drama entries to the database.

        Args:
            drama_list (list): List of drama information dictionaries.
        """
        for drama_info in drama_list:
            if drama_id := drama_info.get("id", False):
                if not self.contains_id(drama_id):
                    self.add_drama(drama_info)

        self.save()


database = DramaDatabase()