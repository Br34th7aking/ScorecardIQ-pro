FILEPATH = "/Users/abhijitraj/Downloads/odis_male_json/1389388.json"

# Fantasy Points System
FANTASY_POINTS = {
  'ODI': {
    'RUNS': 1,
    'FOUR_BONUS': 1,
    'SIX_BONUS': 2,
    'HALF_CENTURY_BONUS': 4,
    'CENTURY_BONUS': 8,
    'DUCK_PENALTY': -3, # should be applied only to batter, wicket-keeper, all-rounder
    'WICKET': 25,
    'LBW_BONUS': 8,
    'BOWLED_BONUS': 8,
    'FOUR_WICKET_BONUS': 4,
    'FIVE_WICKET_BONUS': 8,
    'MAIDEN_OVER': 4,
    'CATCH': 8,
    'THREE_CATCH_BONUS': 4,
    'STUMPING': 12,
    'RUNOUT': 12,
    'INDIRECT_RUNOUT': 6,    
    'ANNOUNCED': 4,
    'SUBSTITUTE': 4,
    # Economy rate points to be applied only if 5 or more overs bowled
    'ECONOMY_UNDER_2.5': 6,
    'ECONOMY_UNDER_3.5': 4,
    'ECONOMY_UNDER_4.5': 2,
    'ECONOMY_OVER_7': -2,
    'ECONOMY_OVER_8': -4,
    'ECONOMY_OVER_9': -6, 
    # Strike rate points to be given only to batters, wicket keepers and all rounders
    # Minimum number of balls to be played = 20
    'OVER_140': 6,
    'OVER_120': 4,
    'OVER_100': 2,
    'UNDER_50': -2,
    'UNDER_40': -4,
    'UNDER_30': -6

  }
}