"""

This is a file with usage examples of both the tasks.

"""


from matchdata_utils import compute_total_distance, compute_total_distance_by_interval, compute_accelerations, \
    load_tracking_data

# edit file paths as needed (relative to the path where the package is run from)
TRACKING_FILE_PATH = "../data/OneDrive_1_13-6-2025/data-tracking/tracking-produced.jsonl"
METADATA_FILE_PATH = "../data/OneDrive_1_13-6-2025/data-tracking/metadata.json"

df = load_tracking_data(TRACKING_FILE_PATH)
print(df.columns)
print(df.shape[0])


df_total_dist = compute_total_distance(df)
print(df_total_dist.columns)
print(df_total_dist.head())
print(df_total_dist.shape[0])


speed_intervals = [(1.5, 2), (2, 3), (2.5, None),]
df_dist_speed_intervals = compute_total_distance_by_interval(df, speed_intervals)
print(df_dist_speed_intervals.head())
print(df_dist_speed_intervals.columns)
print(df_dist_speed_intervals.shape[0])


accelerations_df = compute_accelerations(df, threshold=7.5)
print(accelerations_df.head())
print(accelerations_df.shape[0])
