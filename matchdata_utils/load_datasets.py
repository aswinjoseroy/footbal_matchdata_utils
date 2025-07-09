"""
TASK 01: Loading and storing datasets.


"""

import pandas as pd
import json


def load_metadata(metadata_file):
    """

    :param metadata_file: metadata json file path
    :return: DF with expected columns

    """
    with open(metadata_file, 'r') as file_handler:
        data = json.load(file_handler)

    match_data = data['data']

    home_team_id = match_data['homeTeam']['id']
    away_team_id = match_data['awayTeam']['id']

    home_team_players = match_data['homeTeam']['players']
    away_team_players = match_data['awayTeam']['players']

    for player in home_team_players:
        player['team_id'] = home_team_id
    for player in away_team_players:
        player['team_id'] = away_team_id

    all_players = home_team_players + away_team_players

    df = pd.DataFrame(all_players)
    df = df[['team_id', 'id', 'name', 'position', 'number']]
    df.columns = ['team_id', 'player_id', 'player_name', 'player_position', 'player_number']

    return df


# df = load_metadata('../data/OneDrive_1_13-6-2025/data-tracking/metadata.json')
# print(df.columns)


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


# df = load_tracking_data("../data/OneDrive_1_13-6-2025/data-tracking/tracking-produced.jsonl")
# print(df.columns)


def write_df_to_parquet(df, output_file_name):
    """

    :param df: A Pandas DataFrame to write to disk.
    :param output_file_name: Path to the output .parquet file.
    :return: None

    Note: partition columns can also be specified, as needed to optimise storage and reads.
    """

    df.to_parquet(output_file_name, index=False)
    return None
