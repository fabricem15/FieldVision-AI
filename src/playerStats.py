from pybaseball import pybaseball, pitching_stats, batting_stats, playerid_reverse_lookup
import pandas as pd
import numpy as np

class PlayerStats:
    useful_pitcher_stats = [
    'IDfg',
    'Season',
    "AVG",      # Batting Average
    "HR",       # Home Runs
    "K%",       # Strikeout Rate
    "BB%",      # Walk Rate
    "LOB%",     # Left on Base Percentage
    "HR/FB",    # Home Run per Fly Ball
    "GB%",      # Ground Ball Percentage
    "FB%",      # Fly Ball Percentage
    "LD%",      # Line Drive Percentage
    "SwStr%",   # Swinging Strike Percentage
    "Zone%",    # Pitches in the Strike Zone
    "O-Swing%", # Outside the Zone Swing Percentage
    "Z-Swing%", # Inside the Zone Swing Percentage
    "Swing%",   # Overall Swing Percentage
    "O-Contact%", # Outside the Zone Contact Percentage
    "Z-Contact%", # Inside the Zone Contact Percentage
    "Contact%",  # Overall Contact Percentage
    "F-Strike%", # First-pitch Strike Percentage
    "K/9", #Strikeouts per 9 innings
    "HR/9", #Hometruns per 9 innings
    "ERA", #Earned run Average
    "CSW%",     # Called Strikes + Whiffs Percentage
    ]

    useful_batter_stats = [
    'IDfg',
    'Season',
    "AVG",        # Batting Average
    "SLG",        # Slugging Percentage
    "OPS",        # On-Base Plus Slugging
    "ISO",        # Isolated Power
    "LD%",        # Line Drive Percentage
    "GB%",        # Ground Ball Percentage
    "FB%",        # Fly Ball Percentage
    "HR/FB",      # Home Run per Fly Ball
    "O-Swing%",   # Swings at pitches outside the strike zone
    "Z-Swing%",   # Swings at pitches inside the strike zone
    "Swing%",     # Overall swing percentage
    "O-Contact%", # Contact on pitches outside the strike zone
    "Z-Contact%", # Contact on pitches inside the strike zone
    "Contact%",   # Overall contact percentage
    "Zone%",      # Pitches seen in the strike zone
    "SwStr%",     # Swinging strike percentage
    "F-Strike%",  # First-pitch strike percentage
    "Pull%",      # Pull Percentage
    "Cent%",      # Center Percentage
    "Oppo%",      # Opposite Field Percentage
    "Hard%",      # Hard Contact Percentage
    "Med%",        # Medium Contact Percentage
    "Soft%",      # Soft Contact Percentage
    ]

    # Data Constants
    start_date = "2019-04-01" #start of 2023 season
    end_date = "2023-05-01" #end of 2023 seaon
    test_start_date = "2023-07-01"
    test_end_date = "2023-07-30"

    # Hyper Params
    size = 125
    scale = size/250
    num_grid_squares = size * size
    
    pitcher_cache = {}
    batter_cache = {}

    def __init__(self):
        pybaseball.cache.enable()
        self.pitcher_cache[2024] = pitching_stats(2024, qual=1)[self.useful_pitcher_stats]
        self.batter_cache[2024] = batting_stats(2024, qual=1)[self.useful_batter_stats]
        self.pitcher_cache[2023] = pitching_stats(2023, qual=1)[self.useful_pitcher_stats]
        self.batter_cache[2023] = batting_stats(2023, qual=1)[self.useful_batter_stats]


    def addPitcherBatterData(self, events):
        all_pitchers = events['pitcher'].unique()
        all_batters = events['batter'].unique()

        # 1. Pre-fetch all pitcher and batter data
        pitcher_data = []
        batter_data = []

        for season in events['game_year'].unique():
            if season not in self.pitcher_cache:
                self.pitcher_cache[season] = pitching_stats(season, qual=1)[self.useful_pitcher_stats]
                self.batter_cache[season] = batting_stats(season, qual=1)[self.useful_batter_stats]
            pitcher_data.append(self.pitcher_cache[season])
            batter_data.append(self.batter_cache[season])

        pitcher_data = pd.concat(pitcher_data)
        batter_data = pd.concat(batter_data)

        # add prefix to all columns
        pitcher_data.columns = ['pitcher_' + col for col in pitcher_data.columns]
        batter_data.columns = ['batter_' + col for col in batter_data.columns]

        # 2. Create DataFrames for efficient merging
        all_pitcher_info = playerid_reverse_lookup(all_pitchers, key_type='mlbam')[['key_mlbam', 'key_fangraphs']]
        all_batter_info = playerid_reverse_lookup(all_batters, key_type='mlbam')[['key_mlbam', 'key_fangraphs']]

        # Handle cases where playerid_reverse_lookup returns empty results
        if all_pitcher_info.empty:
            # Handle this case, e.g., by logging an error or returning an empty DataFrame
            return pd.DataFrame(), "Error: No matching pitcher IDs found."

        if all_batter_info.empty:
            return pd.DataFrame(), "Error: No matching batter IDs found."

        # Drop events with missing pitcher or batter
        events = events.dropna(subset=['pitcher', 'batter'])

        # 3. Update event to include key_fangraphs (with renaming)
        events = events.merge(all_pitcher_info, left_on='pitcher', right_on='key_mlbam', how='left')
        events = events.rename(columns={'key_fangraphs': 'pitcher_fangraph'})
        events = events.merge(all_batter_info, left_on='batter', right_on='key_mlbam', how='left')
        events = events.rename(columns={'key_fangraphs': 'batter_fangraph'})
        events = events.drop(columns=['key_mlbam_x', 'key_mlbam_y'])

        # 4. Merge event and pitcher/batter stats, handling missing data
        events = events.merge(pitcher_data, left_on=['game_year', 'pitcher_fangraph'],
                                    right_on=['pitcher_Season', 'pitcher_IDfg'], how='left', indicator='pitcher_merge')
        events = events.merge(batter_data, left_on=['game_year', 'batter_fangraph'],
                                        right_on=['batter_Season', 'batter_IDfg'], how='left', indicator='batter_merge')

        # Remove rows where either pitcher or batter stats are missing
        events = events[
            (events['pitcher_merge'] == 'both') & (events['batter_merge'] == 'both')
        ]

        # Drop the no longer needed columns
        columnsToRemove = ['pitcher_merge', 'batter_merge', 'game_year', 'batter', 'pitcher', 'pitcher_fangraph', 'pitcher_Season', 'pitcher_IDfg', 'batter_fangraph','batter_IDfg', 'batter_Season']
        events.drop(columns=columnsToRemove, inplace=True)

        return events, None

    def process_data(self, events):
        # Bases loaded one hot
        for base in ['on_1b', 'on_2b', 'on_3b']:
            events[base] = events[base].notna().astype(int)

        # Score differential (direct calculation)
        events['score_dif'] = events['bat_score'] - events['fld_score']

        # Convert stand and type (vectorized with map)
        events['stand'] = events['stand'].map({'L': 0, 'R': 1})

        # Drop the unnecessary columns
        events.drop(columns=['bat_score', 'fld_score'], errors='ignore', inplace=True)
        return events

    def getDataForModel(self, game_year, pitcher, batter, inning, stand, balls, strikes, on_1b, on_2b, on_3b, pitch_number, bat_score, field_score):
        # Create a pandas DataTable where each input is in the table under the name of its varaible
        events = pd.DataFrame({
            'game_year': [game_year],
            'batter': [batter],
            'pitcher': [pitcher],
            'inning': [inning],
            'stand': [stand],
            'balls': [balls],
            'strikes': [strikes],
            'on_1b': [None if on_1b == 0 else on_1b],
            'on_2b': [None if on_2b == 0 else on_2b],
            'on_3b': [None if on_3b == 0 else on_3b],
            'pitch_number': [pitch_number],
            'bat_score': [bat_score],
            'fld_score': [field_score]
        })
        # check if the return value is null first.
        # events, error = self.addPitcherBatterData(events)
        try:
            events, error = self.addPitcherBatterData(events)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
        if (len(events) == 0):
            print("No data found for the given dates")
            return None
            # return Exception("No data found for the given dates")

        event = self.process_data(events).values.astype(np.float32)
        # Check if any value if null
        if event is None:
            return None
        else:
            return event[0]  