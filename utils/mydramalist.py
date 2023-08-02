import requests

class MyDramaList:
    def __init__(self) -> None:
        """
        Initialize a new instance of the MyDramaList class.
        """
        self.session = requests.Session()

    def get_dramas(self, drama: str) -> dict or bool:
        """
        Get information about dramas from the MyDramaList API.

        Args:
            drama (str): ID of the drama.

        Returns:
            dict or bool: A dictionary containing drama information if successful, or False if the request fails.
        """
        drama_data = self.session.get(
            f"https://api.mydramalist.com/v1/titles/{drama}",
            headers={'Content-Type': 'application/json', 'mdl-api-key': 'bac0925df628dce7841a1d4e8d474c2e63fb818b'}
        )
        return drama_data.json() if drama_data.ok else False


mydramalist = MyDramaList()
