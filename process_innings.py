import json
from config import config
from wicket import wicket

######################
#  helper functions  #
######################

# delivery related functions


def get_batter(delivery):
    pass


def get_bowler(delivery):
    pass


def get_nonstriker(delivery):
    pass


def get_runs(delivery):
    pass


def get_extras(delivery):
    pass


def get_replacements(delivery):
    pass


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


def get_innings_data(inning):
    print("Processing first innings")
    dots = 0
    singles = 0
    doubles = 0
    threes = 0
    boundaries = 0
    other = 0
    total_deliveries = 0
    for over in inning:
        deliveries_in_over = over["deliveries"]
        for delivery in deliveries_in_over:
            delivery_keys = delivery.keys()
            total_deliveries += 1
            if delivery["runs"]["total"] == 0:
                dots += 1
            elif delivery["runs"]["total"] == 1 and delivery["runs"]["extras"] == 0:
                singles += 1
            elif delivery["runs"]["total"] == 2 and delivery["runs"]["extras"] == 0:
                doubles += 1
            elif delivery["runs"]["total"] >= 4 and delivery["runs"]["extras"] == 0:
                boundaries += 1
            elif delivery["runs"]["total"] == 3 and delivery["runs"]["extras"] == 0:
                threes += 1
            else:
                other += 1
                # print(delivery['runs'])

            if "wickets" in delivery_keys:
                wickets = get_wickets(delivery)
                for item in wickets:
                    print(item)

    # print("Total deliveries bowled", total_deliveries)
    # print("Total dots", dots)
    # print("Total singles", singles)
    # print("Total doubles", doubles)
    # print("Total boundaries", boundaries)
    # print("Others", other)
    # print("Over", inning[0])


def process():
    with open(config.FILEPATH, "r") as input_file:
        data = json.load(input_file)
        print(data.keys())
        if "innings" in data.keys():
            get_innings_data(data["innings"][0]["overs"])


process()
