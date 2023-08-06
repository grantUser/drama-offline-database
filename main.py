import json

from utils.mydramalist import mydramalist
from utils.step import step

with open("drama-database.json", "r") as database_file:
    database = json.load(database_file)

if currentStep := step.get_step():
    currentStep = int(currentStep) + 1
    limit = currentStep + 1000

    characters = {}
    for number in range(currentStep, limit):
        step.set_step(str(number))

        if drama := mydramalist.get_dramas(number):
            if "id" in drama:
                synonyms = drama["alt_titles"]
                if drama["original_title"] not in synonyms:
                    synonyms.append(drama["original_title"])

                tags = drama["tags"] + drama["genres"]

                drama_dict = {}

                drama_dict["id"] = drama["id"]

                drama_dict["sources"] = []
                if "sources" in drama:
                    drama_dict["sources"] = drama["sources"]

                drama_dict["title"] = ""
                if "title" in drama:
                    drama_dict["title"] = drama["title"]

                drama_dict["type"] = ""
                if "type" in drama:
                    drama_dict["type"] = drama["type"]

                drama_dict["episodes"] = ""
                if "episodes" in drama:
                    drama_dict["episodes"] = drama["episodes"]

                drama_dict["status"] = ""
                if "status" in drama:
                    drama_dict["status"] = drama["status"]

                drama_dict["year"] = ""
                if "year" in drama:
                    drama_dict["year"] = drama["year"]

                drama_dict["picture"] = ""
                if "images" in drama:
                    if "poster" in drama["images"]:
                        drama_dict["picture"] = drama["images"]["poster"]
                
                drama_dict["thumbnail"] = ""
                if "images" in drama:
                    if "thumb" in drama["images"]:
                        drama_dict["thumbnail"] = drama["images"]["thumb"]
                    
                drama_dict["synonyms"] = synonyms
                drama_dict["tags"] =  tags

                database.append(drama_dict)

with open("drama-database.json", "w") as database_file:
    json.dump(database, database_file, separators=(',',':'))
