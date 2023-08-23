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
    
    def clean(self) -> None:
        """
        Clean the drama entries in the database by removing unauthorized keys.

        This method iterates through each drama entry in the database and removes
        any keys that are not present in the list of allowed keys.
        """
        allowed_keys = ["id", "sources", "title", "type", "episodes", "status", "year", "picture", "thumbnail", "synonyms", "tags"]
        for dictionary in self._database:
            keys_to_remove = [key for key in dictionary if key not in allowed_keys]
            
            for key in keys_to_remove:
                dictionary.pop(key)

            tags = dictionary.get("tags", [])
            cleaned_tags = []

            for tag in tags:
                if isinstance(tag, dict):
                    tag_name = tag.get("name")
                    if tag_name:
                        cleaned_tags.append(tag_name)
                else:
                    cleaned_tags.append(tag)

            dictionary["tags"] = cleaned_tags

        self.save()

    def update(self, drama_id: int, new_data: dict) -> None:
        """
        Update a drama entry in the database with new data.

        Args:
            drama_id (int): The ID of the drama to be updated.
            new_data (dict): New data to update the drama entry with.
        """
        for entry in self._database:
            if entry.get("id") == drama_id:
                synonyms = new_data.get("alt_titles", [])

                if new_data.get("original_title", False):
                    synonyms = synonyms + list(new_data.get("original_title", ""))

                tags = []
                if isinstance(new_data.get("tags"), list):
                    for tag in tags:
                        if isinstance(tag, dict):
                            if "name" in tag:
                                tags.append(tag.get("name"))
                        else:
                            tags.append(tag)

                genres = []
                if isinstance(new_data.get("genres"), list):
                    for genre in genres:
                        if isinstance(genre, dict):
                            if "name" in genre:
                                genres.append(genre.get("name"))
                        else:
                            genres.append(genre)

                tags = list(tags) + list(genres)
        
                updated_data = {
                    "id": new_data.get("id", ""),
                    "sources": new_data.get("sources", []),
                    "title": new_data.get("title", ""),
                    "type": new_data.get("type", ""),
                    "episodes": new_data.get("episodes", ""),
                    "status": new_data.get("status", ""),
                    "year": new_data.get("year", ""),
                    "picture": new_data.get("images", {}).get("poster", ""),
                    "thumbnail": new_data.get("images", {}).get("thumb", ""),
                    "synonyms": synonyms,
                    "tags": tags,
                }

                entry.update(updated_data)
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
            for tag in tags:
                if isinstance(tag, dict):
                    if "name" in tag:
                        tags.append(tag.get("name"))
                else:
                    tags.append(tag)

        genres = []
        if isinstance(drama_info.get("genres"), list):
            for genre in genres:
                if isinstance(genre, dict):
                    if "name" in genre:
                        genres.append(genre.get("name"))
                else:
                    genres.append(genre)

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