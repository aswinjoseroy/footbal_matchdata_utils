**Approach:**

Author: Aswin Jose Roy

Understanding of the objective: The objective is to process player tracking data to compute performance metrics such as total distance covered, distance by speed intervals, and number of accelerations above a given threshold. Apart from these, as a preliminary step, the datasets have to be loaded as dataframes for further processing.  

Each core computation is a separate function to promote readability and testability, apart from seprating the two different tasks into seprate python files for readability. The codebase is organized as an installable library (steps to install follow). 


**File Structure**

Both tasks can be found under `matchdata_utils/load_datasets.py` and `matchdata_utils/compute_player_stats.py`, respectively. 

`pyproject.toml` is the setup file (to install as a package). 


**Libraries and Environment**

The library has been developed and tested in python version `3.12.11`, as instructed. 

The library uses `Pandas` along with the standard `json` library to load the data and for manipulations. For computations, `numpy` is used. 

**Method**


`compute_total_distance(df)
`

Computes the cumulative Euclidean distance (sqrt(x² + y²)) for each player (group by `player_id`) traveled during the match. 


`compute_total_distance_by_interval(df, speed_intervals)
`

Accepts speed intervals as tuples (e.g., (1.5, 2) or (2.5, None)) within a list. 

* Sorted the data chronologically and used .shift() within player groups to calculate distances between consecutive frames.
* Aggregated total distance per player and applied flexible filtering to compute distances within specified speed intervals.
* Returned one row per player, with each column representing distance covered in a different speed range. Each column will be named with a prefix 'distance_*' with a text that follows indicating the range.   

`compute_accelerations(df, threshold)
`

Detects acceleration bursts where a player’s speed crosses upward past the threshold (e.g., from below 2.5 m/s to above). 

**Assumptions made:** 

1. The current implementation of functionalities within task 02 (computations) returns results only for players who meet the specified conditions (e.g., have speeds above a threshold or fall within given intervals) . If a full list of players — including those with no qualifying data — is needed, an outer join with a complete player list can be incorporated as an additional step (by loading metadata using `load_metadata`). This is not currently done as the task description does not explicitly ask for this.  
2. An acceleration event is assumed to be: A valid acceleration event is when a player's speed goes from below to above the threshold (crossing it upward). Does not require computing true acceleration (i.e., rate of change of speed over time) — just crossings. 
3. The input datasets are already structured and cleaned with columns: `'period_id', 'frame_index', 'game_clock', 'wall_clock', 'player_id', 'player_number', 'speed', 'x', 'y', 'z'`.
4. Tracking data is at regular intervals and ordered within frame_index (per player).



**Potential improvements for next iteration:**

1. Add unit tests or validations (e.g., speed range checks, distance sanity checks).
2. Add defensive handling (empty DF inputs, incorrect column data formats, return datatype etc. ).
3. Include a util method to get all player ids and encapsulate the differnt compute methods with this exhaustive list adding empty values where no results are present. 


**Installing Library and Usage**

The package can be installed as a library within a Python 3.12 environment. Type in the following command to install the package in your local interpreter / python3 environment:

    pip3 install -e .
    
Once the package is succesfully installed, we can use it as a library from any project in the system. 
A quick example usage once the package is installed is: 

    `from matchdata_utils import compute_total_distance, compute_accelerations
    from matchdata_utils import load_tracking_data
    
    df = load_tracking_data("path/to/file.jsonl")
    result_df = compute_total_distance(df)
    `

More detailed examples of usage can be found in the `matchdata_utils/main.py` python file. 



