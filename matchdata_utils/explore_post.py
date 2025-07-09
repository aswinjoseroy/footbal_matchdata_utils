import pandas as pd
import json


def load_tracking_data(tracking_data_file):
    """

    :param tracking_data_file: path to the tracking dataset /  jsonl file
    :return: DF with expected columns
    """
    tracking_data_rows = []

    with open(tracking_data_file, 'r') as file_handler:
        # parse each line
        for each_json_line in file_handler:
            each_line_dict = json.loads(each_json_line)

            period_id = each_line_dict.get("period")
            frame_index = each_line_dict.get("frameIdx")
            game_clock = each_line_dict.get("gameClock")
            wall_clock = each_line_dict.get("wallClock")

            for team in ["homePlayers", "awayPlayers"]:
                players = each_line_dict.get(team, [])
                for player in players:
                    player_id = player.get("playerId")
                    player_number = player.get("number")
                    speed = player.get("speed", 0.0)
                    x, y, z = player.get("xyz", [None, None, None])

                    tracking_data_rows.append({
                        "period_id": period_id,
                        "frame_index": frame_index,
                        "game_clock": game_clock,
                        "wall_clock": wall_clock,
                        "player_id": player_id,
                        "player_number": player_number,
                        "speed": speed,
                        "x": x,
                        "y": y,
                        "z": z
                    })

    df = pd.DataFrame(tracking_data_rows)
    return df


df = load_tracking_data("../data/OneDrive_1_13-6-2025/data-tracking/tracking-produced.jsonl")

# Distinct values for period_id
print("Unique period_id values:", df['period_id'].unique())

# Distinct values for frame_index
print("Unique frame_index values:", df['frame_index'].unique())

# Step 1: Get the first available period_id and frame_index
first_period_id = df['period_id'].iloc[0]
first_frame_index = df['frame_index'].iloc[0]

# Step 2: Filter the DataFrame for this combination
first_frame_df = df[
    (df['period_id'] == first_period_id) &
    (df['frame_index'] == first_frame_index)
]

# Step 3: Extract all player IDs for this frame
player_ids = first_frame_df['player_id'].unique()

print(f"Player IDs for period {first_period_id}, frame index {first_frame_index}:")
print(len(player_ids))
