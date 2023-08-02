import json

from utils.mydramalist import mydramalist
from utils.step import step

with open("drama-database.json", "r") as database_file:
    database = json.load(database_file)

if currentStep := step.get_step():
    currentStep = int(currentStep) + 1
    limit = currentStep + 200

    characters = {}
    for number in range(currentStep, limit):
        step.set_step(str(number))

        if drama := mydramalist.get_dramas(number):
            if "id" in drama:
                synonyms = drama["alt_titles"]
                if drama["original_title"] not in synonyms:
                    synonyms.append(drama["original_title"])

                tags = drama["tags"] + drama["genres"]


                drama_dict = {
                    "sources": drama["sources"],
                    "title": drama["title"],
                    "type": drama["type"],
                    "episodes": drama["episodes"],
                    "status": drama["status"],
                    "year": drama["year"],
                    "picture": drama["images"]["poster"],
                    "thumbnail": drama["images"]["thumb"],
                    "synonyms": synonyms,
                    "tags": tags
                }

                database.append(drama_dict)

with open("drama-database.json", "w") as database_file:
    json.dump(database, database_file, separators=(',',':'))
