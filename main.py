import datetime
from typing import List, Dict
from utils.mydramalist import mydramalist

class DramaManager:
    def __init__(self):
        """
        Initialize the DramaManager instance.
        """
        self.current_year = datetime.datetime.now().year
        self.next_year = self.current_year + 1

    def fetch_yearly_dramas(self, year: int) -> List[Dict]:
        """
        Fetch dramas for a specific year.

        Args:
            year (int): The year for which to fetch dramas.

        Returns:
            List[Dict]: List of dictionaries representing dramas.
        """
        return mydramalist.get_dramas_by_year(year=year)

    def add_dramas_to_database(self, dramas: List[Dict]):
        """
        Add a list of dramas to the database.

        Args:
            dramas (List[Dict]): List of dictionaries representing dramas.
        """
        mydramalist.database.add_bulk_dramas(dramas)

    def fetch_and_add_new_dramas(self):
        """
        Fetch new dramas' episodes and add them to the database.
        """
        episodes = mydramalist.get_dramas_episodes()
        new_dramas = []

        for episode in episodes:
            episode_id = episode.get("rid")
            if episode_id and not mydramalist.database.contains_id(episode_id):
                if new_drama := mydramalist.get_dramas(episode_id):
                    new_dramas.append(new_drama)

        if new_dramas:
            self.add_dramas_to_database(new_dramas)

    def fetch_and_update_dramas(self):
        """
        Fetch recent drama updates and update the database.
        """
        updates = mydramalist.get_dramas_updates_from_yesterday()

        for update in updates:
            update_id = update.get("id")
            if update_id and mydramalist.database.contains_id(update_id):
                if updated_drama := mydramalist.get_dramas(update_id):
                    mydramalist.database.update(update_id, updated_drama)

    def run(self):
        """
        Run the drama management process.
        """
        current_year_dramas = self.fetch_yearly_dramas(self.current_year)
        next_year_dramas = self.fetch_yearly_dramas(self.next_year)
        
        self.add_dramas_to_database(current_year_dramas)
        self.add_dramas_to_database(next_year_dramas)
        
        self.fetch_and_add_new_dramas()
        self.fetch_and_update_dramas()

        mydramalist.database.clean()

if __name__ == "__main__":
    manager = DramaManager()
    manager.run()
