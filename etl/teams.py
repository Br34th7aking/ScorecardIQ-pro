# To collect the details of teams available in the cricsheet data
from etlconfig import config
import json
import os
from db import db

def extract_team_names(folder_path: str):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path) and file_path.endswith("json"):
            with open(file_path, "r") as input_file:
                data = json.load(input_file)["info"]
                if "team_type" in data.keys():
                    if "teams" in data.keys():
                        kind = data["team_type"]
                        query = "SELECT name from scorecard_team"
                        queried_result = db.execute(query)
                        teams_already_present = [x[0] for x in queried_result]
                        for team in data["teams"]:
                          if team not in teams_already_present:
                            query = f"INSERT INTO scorecard_team (name, kind) VALUES('{team}', '{kind}');"
                            db.insert(query)


if __name__ == "__main__":
    folder_path = config.FOLDER_PATH
    extract_team_names(folder_path)
