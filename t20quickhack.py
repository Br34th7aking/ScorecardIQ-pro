import os
import json
from config import config
from wicket import wicket
import pandas as pd
import sys
######################
#  helper functions  #
######################

# delivery related functions


def get_batter(delivery):
    return delivery["batter"]


def get_bowler(delivery):
    return delivery["bowler"]


def get_nonstriker(delivery):
    return delivery["non_striker"]


def get_runs(delivery):
    pass


def get_extras(delivery):
    pass


def get_replacements(delivery):
    pass


def is_wide(delivery):
    if "extras" in delivery.keys():
        if "wides" in delivery["extras"].keys():
            return True
    return False


def is_noball(delivery):
    if "extras" in delivery.keys():
        if "noballs" in delivery["extras"].keys():
            return True
    return False


def calculate_strike_rate(batter):
    if batter['balls_faced'] > 0:
        return round(batter["runs"] * 100 / batter["balls_faced"], 2)
    return 0


def update_batting_bonus(batter):
    if batter["runs"] >= 100:
        return "100 run bonus"
    elif batter["runs"] >= 50:
        return "50 run bonus"
    elif batter["runs"] >= 30:
        return "30 run bonus"
    else:
        return "NA"


def is_out_on_duck(batter):
    if batter["runs"] == 0:
        return "Yes"
    return "No"


def calculate_economy_rate(bowler):
    if bowler["overs_bowled"] > 0:
        return round(bowler["runs_conceded"] / bowler["overs_bowled"], 2)
    return 0


def credit_wicket_to_bowler(wicket):
    bowler_wicket_types = [
        "bowled",
        "caught",
        "caught and bowled",
        "lbw",
        "hit wicket",
        "stumped",
    ]
    if wicket["kind"] in bowler_wicket_types:
        return True
    return False


def caught_and_bowled_bonus(wicket):
    if wicket["kind"] == "caught and bowled":
        return 1
    return 0


def get_wickets(delivery):
    wickets = []
    for item in delivery["wickets"]:
        kind = item["kind"]
        player_out = item["player_out"]
        fielders = []
        if "fielders" in item.keys():
            for fielder in item["fielders"]:
                fielders.append(fielder["name"])

        wickets.append(wicket.Wicket(kind, player_out, fielders))
    return wickets


def calculate_lbw_bowled_bonus(wickets):
    number_of_bonuses = 0
    for wicket in wickets:
        if wicket["kind"] == "lbw" or wicket["kind"] == "bowled":
            number_of_bonuses += 1
    return number_of_bonuses


def get_players(team_players):
    teams = team_players.keys()
    players = {}
    for team in teams:
        player_list = team_players[team]
        for player in player_list:
            players[player] = {
                "bat_first": 0,
                "bat_pos": 0,
                "bowl_pos": 0,
                "announced_or_substitute": "announced",
                "dots": 0,
                "ones": 0,
                "twos": 0,
                "threes": 0,
                "runs": 0,
                "fours": 0,  # only consider boundary 4's. Non-boundary 4's are directly added to the runs
                "sixes": 0,
                "strike_rate": 0,
                "balls_faced": 0,
                "batting_bonus": 0,
                "duck": 0,
                "legal_balls_bowled": 0,
                "overs_bowled": 0,
                "wickets": 0,
                "lbw_bowled_bonus": 0,
                "multi_wicket_bonus": 0,
                "maiden_over": 0,
                "runs_conceded": 0,
                "economy_rate": 0,
                "catch": 0,
                "catch_bonus": 0,
                "runout": 0,
                "stumping": 0,
                "indirect_runout": 0,
                "dismissal_kind": "",
            }
    return players


def get_innings_data(inning, players, first_innings=False):
    total_deliveries = 0
    fielders = {}
    bat_position = 1
    bowl_position = 1
    batters_so_far = []
    bowlers_so_far = []
    for over in inning:
        maiden_over = 1
        deliveries_in_over = over["deliveries"]
        for delivery in deliveries_in_over:
            delivery_keys = delivery.keys()
            batter = delivery["batter"]
            non_striker = delivery["non_striker"]
            bowler = delivery["bowler"]
            if batter not in batters_so_far:
                batters_so_far.append(batter)
                players[batter]["bat_pos"] = bat_position
                bat_position += 1
                if non_striker not in batters_so_far:
                    batters_so_far.append(non_striker)
                    players[non_striker]["bat_pos"] = bat_position
                    bat_position += 1
            if bowler not in bowlers_so_far:
                bowlers_so_far.append(bowler)
                players[bowler]["bowl_pos"] = bowl_position
                bowl_position += 1
            if first_innings:
                players[batter]["bat_first"] = 1
            if not is_wide(delivery):
                # wide is not counted in batter's tally of balls faced
                players[batter]["balls_faced"] += 1
                total_deliveries += 1

            if not is_wide(delivery) and not is_noball(delivery):
                players[bowler]["runs_conceded"] += delivery["runs"]["batter"]
                players[bowler]["legal_balls_bowled"] += 1
                players[bowler]["overs_bowled"] = (
                    players[bowler]["legal_balls_bowled"] / 6
                )

            elif is_wide(delivery):
                players[bowler]["runs_conceded"] = delivery["extras"]["wides"]

            elif is_noball(delivery):
                players[bowler]["runs_conceded"] = delivery["extras"]["noballs"]

            if delivery["runs"]["batter"] > 0 or is_noball(delivery) or is_wide(delivery):
                maiden_over = 0

            if delivery["runs"]["batter"] == 0:
                players[batter]["dots"] += 1
            elif delivery["runs"]["batter"] == 1:
                players[batter]["ones"] += 1
            elif delivery["runs"]["batter"] == 2:
                players[batter]["twos"] += 1
            elif delivery["runs"]["batter"] == 3:
                players[batter]["threes"] += 1
            elif delivery["runs"]["batter"] == 4:
                players[batter]["fours"] += 1
            elif delivery["runs"]["batter"] == 6:
                players[batter]["sixes"] += 1
            else:
                pass
            players[batter]["runs"] += delivery["runs"]["batter"]
            players[batter]["strike_rate"] = calculate_strike_rate(players[batter])
            players[batter]["batting_bonus"] = update_batting_bonus(players[batter])
            players[batter]["duck"] = is_out_on_duck(
                players[batter]
            )  # need to optimize this

            players[bowler]["economy_rate"] = calculate_economy_rate(players[bowler])
            if "wickets" in delivery_keys:
                # wickets = get_wickets(delivery)
                wickets = delivery["wickets"]
                players[bowler]["lbw_bowled_bonus"] += calculate_lbw_bowled_bonus(
                    wickets
                )
                for wicket in wickets:
                    player_out = wicket["player_out"]
                    dismissal_kind = wicket["kind"]
                    players[player_out]["dismissal_kind"] = dismissal_kind
                    players[player_out]["dismissed"] = 1

                    if credit_wicket_to_bowler(wicket):
                        players[bowler]["wickets"] += 1
                        if dismissal_kind == "caught and bowled":
                            players[bowler]["catch"] += 1

                    # fielders
                    if "fielders" in wicket.keys():
                        # print(wicket)
                        fielders = []
                        for fielder in wicket["fielders"]:
                            if "name" in fielder.keys():
                                fielders.append(fielder["name"])
                        if len(fielders) > 1:
                            # this is a case of indirect runout
                            for item in fielders[-2:]:
                                try:
                                    players[item]["indirect_runout"] += 1
                                except:
                                    pass
                        else:
                            if dismissal_kind == "run out":
                                # print(wicket)
                                try:
                                    players[fielders[0]]["runout"] += 1
                                except:
                                    pass # substitute fielder
                            elif dismissal_kind == "caught":
                                try:
                                    players[fielders[0]]["catch"] += 1
                                except:
                                    # this may be a subsitute fielder
                                    # print(fielders)
                                    pass
        players[bowler]["maiden_over"] += maiden_over


def process(filename):
    # match_id = config.FILEPATH.split("/")[-1]
    match_id = filename.split("/")[-1]
    with open(filename, "r") as input_file:
        data = json.load(input_file)
        # print(data.keys())
        players = {}
        if "info" in data.keys():
            players = get_players(data["info"]["players"])
        if "innings" in data.keys():
            # only if both innings happened. later we will check the match result
            if (len(data["innings"]) > 1):
                get_innings_data(data["innings"][0]["overs"], players, first_innings=True)
                get_innings_data(data["innings"][1]["overs"], players)
            else: 
                return

        # df = pd.DataFrame.from_dict(players, orient='index')
        # print(df.head())
        # fantasy points
        for player in players:
            players[player]['fantasy_points'] = 4
            # batting
            players[player]['fantasy_points'] += players[player]['runs']
            players[player]['fantasy_points'] += players[player]['fours']
            players[player]['fantasy_points'] += players[player]['sixes'] * 2
            if players[player]['batting_bonus'] == '30 run bonus':
                players[player]['fantasy_points'] += 4
            elif players[player]['batting_bonus'] == '50 run bonus':
                players[player]['fantasy_points'] += 8
            elif players[player]['batting_bonus'] == '100 run bonus':
                players[player]['fantasy_points'] += 16
            if players[player]['duck'] == 'Yes':
                players[player]['fantasy_points'] -= 2

            if players[player]['balls_faced'] > 10:
                if players[player]['strike_rate'] >170:
                    players[player]['fantasy_points'] += 6
                elif players[player]['strike_rate'] > 150:
                    players[player]['fantasy_points'] += 4
                elif players[player]['strike_rate'] > 130:
                    players[player]['fantasy_points'] += 2
                elif players[player]['strike_rate'] < 50:
                    players[player]['fantasy_points'] -= 6
                elif players[player]['strike_rate'] < 60:
                    players[player]['fantasy_points'] -= 4
                elif players[player]['strike_rate'] < 70:
                    players[player]['fantasy_points'] -= 2

            # fielding
            players[player]['fantasy_points'] += 8 * players[player]['catch']
            if players[player]['catch'] >=3 :
                players[player]['fantasy_points'] += 4
            
            players[player]['fantasy_points'] += 12 * players[player]['stumping']
            players[player]['fantasy_points'] += 12 * players[player]['runout']
            players[player]['fantasy_points'] += 6 * players[player]['indirect_runout']

            # bowling
            players[player]['fantasy_points'] += 25 * players[player]['wickets']
            players[player]['fantasy_points'] += 8 * players[player]['lbw_bowled_bonus']
            if players[player]['wickets'] >=5:
                players[player]['fantasy_points'] += 16
            elif players[player]['wickets'] >=4:
                players[player]['fantasy_points'] += 8
            elif players[player]['wickets'] >=3:
                players[player]['fantasy_points'] += 4
            
            players[player]['fantasy_points'] += players[player]['maiden_over'] * 12
            
            if players[player]['overs_bowled'] >= 2:
                if players[player]['economy_rate'] < 5:
                    players[player]['fantasy_points'] += 6
                elif players[player]['economy_rate'] < 6:
                    players[player]['fantasy_points'] += 4
                elif players[player]['economy_rate'] < 7:
                    players[player]['fantasy_points'] += 2
                elif players[player]['economy_rate'] > 12:
                    players[player]['fantasy_points'] -= 6
                elif players[player]['economy_rate'] > 11:
                    players[player]['fantasy_points'] -= 4
                elif players[player]['economy_rate'] > 10:
                    players[player]['fantasy_points'] -= 2
                
        # for player in players: 
            # print(player, players[player]['fantasy_points'])

        # sorted_by_fantasy_points = sorted(players.keys(), key=lambda x: players[x]['fantasy_points'], reverse=True)

        df = pd.DataFrame.from_dict(players, orient='index').reset_index()
        df['player_name'] = df['index']
        df['match_id'] = match_id
        df = df.drop(['index'], axis=1)
        # df.to_csv('test.csv', index=False)
        return df
        # for player in optimal:
            # print(player, players[player])
        # print(df.columns) 


# process()

## Notes ##
# currently we think that only the runs scored by the batter(including overthrows),
# wide and noballs are counted against the bowler.
# need to validate this.
#
#
# because this scorecard lists all players involved, the run out points may not match with
# the fantasy website scorecard
# no way of telling who are the last 2 players in the runout.
# so the fantasy points might be incorrect

if __name__ == '__main__':
    folder_path = '/Users/abhijitraj/Downloads/t20s_json'
    dfs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path) and file_path.endswith('json'):  # Check if it's a file (and not a subdirectory)
            df = process(file_path)
            dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv('t20.csv', index=False)