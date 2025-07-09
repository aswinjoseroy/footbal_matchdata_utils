"""
TASK 02

Computations on the player tracking data; Dependent on the module to load the metadata/tracking datasets;

"""


import pandas as pd
import numpy as np
from matchdata_utils.load_datasets import load_tracking_data


def compute_total_distance(df):
    """

    :param df: tracking data df
    :return: df with one row per player and second column as the total distance by the player
    """
    # sort the dataframe to ensure proper chronological order of player tracking events
    df = df.sort_values(by=['player_id', 'period_id', 'frame_index'])

    # calculate distance between consecutive points for each player
    df[['x_prev', 'y_prev']] = df.groupby('player_id')[['x', 'y']].shift(1)

    # compute the euclidean distance
    df['distance'] = np.sqrt(
        (df['x'] - df['x_prev'])**2 +
        (df['y'] - df['y_prev'])**2
    )

    # replace empty distances with 0; handling first row and other potential empty values
    df['distance'] = df['distance'].fillna(0)

    # sum total distance per player
    result = df.groupby('player_id')['distance'].sum().reset_index()
    result = result.rename(columns={'distance': 'total_distance'})

    return result


def compute_total_distance_by_interval(df, speed_intervals):
    """

    :param df: tracking df
    :param speed_intervals: intervals of speed as a list of Tuples, eg. [(2,3), (3, 4), (4, None), ]
    :return: df with player_id and the various "distance_**" columns that depict the distance covered in those respective speed intervals
    """

    df = df.sort_values(by=['player_id', 'frame_index'])

    # calculate distance between consecutive frames for each player
    df['x_prev'] = df.groupby('player_id')['x'].shift(1)
    df['y_prev'] = df.groupby('player_id')['y'].shift(1)
    df['distance'] = np.sqrt((df['x'] - df['x_prev']) ** 2 + (df['y'] - df['y_prev']) ** 2)
    df = df.dropna(subset=['distance'])

    # assign distances to each interval slots
    interval_dfs_list = []
    for interval in speed_intervals:
        min_speed = interval[0]
        max_speed = interval[1]
        if max_speed is None:
            interval_label = f"distance_above_{min_speed}"
            speed_filter = df['speed'] >= min_speed
        elif min_speed is None:
            interval_label = f"distance_below_{max_speed}"
            speed_filter = df['speed'] <= max_speed
        else:
            interval_label = f"distance_{min_speed}_to_{max_speed}"
            speed_filter = (df['speed'] >= min_speed) & (df['speed'] < max_speed)

        interval_df = df[speed_filter].groupby('player_id')['distance'].sum().reset_index()
        interval_df.rename(columns={'distance': interval_label}, inplace=True)
        interval_dfs_list.append(interval_df)

    # merge all intervals on player_id
    # start with the first DataFrame in the list
    df_total_dist_by_interval = interval_dfs_list[0]

    # iteratively merge the remaining DataFrames
    for interval_df in interval_dfs_list[1:]:
        df_total_dist_by_interval = pd.merge(df_total_dist_by_interval, interval_df, on='player_id', how='outer')

    # fill missing values with 0
    df_total_dist_by_interval = df_total_dist_by_interval.fillna(0)

    return df_total_dist_by_interval


def compute_accelerations(df, threshold):
    """

    :param df: tracking df
    :param threshold: threshold speed used to determine accelrations (see README file for details on assumptions made)
    :return:
    """

    df = df.sort_values(by=['player_id', 'frame_index'])

    # get previous speed shifting to prev frame
    df['prev_speed'] = df.groupby('player_id')['speed'].shift(1)

    # condition to detect transitions from below to above threshold
    acceleration_condition = (df['prev_speed'] < threshold) & (df['speed'] >= threshold)

    # count accelerations per player
    acceleration_df_threshold = df[acceleration_condition].groupby('player_id').size().reset_index(
        name='number_of_accelerations')

    return acceleration_df_threshold


# testing code

# df = load_tracking_data("../data/OneDrive_1_13-6-2025/data-tracking/tracking-produced.jsonl")
# print(df.columns)
# print(df.shape[0])


# df_total_dist = compute_total_distance(df)
# print(df_total_dist.columns)
# print(df_total_dist.head())
# print(df_total_dist.shape[0])


# speed_intervals = [(1.5, 2), (2, 3), (2.5, None),]
# df_dist_speed_intervals = compute_total_distance_by_interval(df, speed_intervals)
# print(df_dist_speed_intervals.head())
# print(df_dist_speed_intervals.columns)
# print(df_dist_speed_intervals.shape[0])


# accelerations_df = compute_accelerations(df, threshold=7.5)
# print(accelerations_df.head())
# print(accelerations_df.shape[0])
