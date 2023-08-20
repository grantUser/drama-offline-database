from datetime import datetime, timedelta

import requests

from utils.database import database


class MyDramaList:
    def __init__(self) -> None:
        """
        Initialize a new instance of the MyDramaList class.
        """
        self.api_key = "bac0925df628dce7841a1d4e8d474c2e63fb818b"

        self.session = requests.Session()
        self.session.headers.update({"mdl-api-key": self.api_key})

        self.database = database

    def get_yesterday_date(self) -> str:
        """
        Get the date of yesterday in the format "YYYY-MM-DD".

        Returns:
            str: The date of yesterday.
        """
        yesterday = datetime.now() - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def get_dramas_updates_from_yesterday(self) -> dict or bool:
        """
        Get information about drama title updates from the MyDramaList API starting from yesterday.

        Returns:
            dict or bool: A dictionary containing title update information if successful, or False if the request fails.
        """
        start_date = self.get_yesterday_date()
        url = f"https://api.mydramalist.com/v1/titles/updates/{start_date}"
        drama_data = self.session.get(url)
        return drama_data.json() if drama_data.ok else False

    def get_dramas(self, drama: str) -> dict or bool:
        """
        Get information about dramas from the MyDramaList API.

        Args:
            drama (str): ID of the drama.

        Returns:
            dict or bool: A dictionary containing drama information if successful, or False if the request fails.
        """
        drama_data = self.session.get(f"https://api.mydramalist.com/v1/titles/{drama}")
        return drama_data.json() if drama_data.ok else False

    def get_dramas_episodes(self) -> dict or bool:
        """
        Get information about upcoming drama episodes from the MyDramaList API.

        Returns:
            dict or bool: A dictionary containing episode information if successful, or False if the request fails.
        """
        drama_data = self.session.post(
            "https://api.mydramalist.com/v1/calendar/episodes"
        )
        return drama_data.json()["items"] if drama_data.ok else False

    def get_dramas_by_year(self, year: int) -> dict or bool:
        """
        Get information about dramas airing throughout a specific year from the MyDramaList API.

        Args:
            year (int): The year for which to retrieve drama information.

        Returns:
            list or bool: A list containing drama information if successful, or False if the request fails.
        """
        dramas = []

        for quarter in ["1", "2", "3", "4"]:
            drama_data_body = {"year": year, "quarter": quarter}
            drama_data = self.session.post(
                "https://api.mydramalist.com/v1/calendar/quarter", json=drama_data_body
            )

            if drama_data.ok:
                dramas.extend(drama_data.json())

        return dramas or False


mydramalist = MyDramaList()
