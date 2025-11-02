import numpy as np
import pandas as pd

"""

MULTI-EVENT POINT FORMULAS

Format:
track (running) events: seconds
field (jumping) events: centimeters
field (throwing) events: meters

Error checks:
- Is base (B - event_time, event_distance - B) negative?
- Are points complex?
- Are points negative?


"""

def track_event_points(multievent: str, event: str, event_time: float, a: float, b: float, c: float) -> int:
    base = b - event_time

    if base < 0:
        raise ValueError(f"Invalid event perforamnce entry: base (B - time) = {base} is negative")
    
    points = a * base ** c

    if np.iscomplex(points):
        raise ValueError(f"Computation produced complex points: {points}")
    if points < 0:
        raise ValueError(f"Invalid event performance entry, results in negative points ({points})")
    
    return int(points)
        



def field_event_points(multievent: str, event: str, event_distance: float, a: float, b: float, c:float) -> int:
    base = event_distance - b

    if base < 0:
        raise ValueError(f"Invalid event performance entry: base (distance - B) = {base} is negative")

    points = a * base ** c

    if np.iscomplex(points):
        raise ValueError(f"Computation produced complex points: {points}")
    if points < 0:
        raise ValueError(f"Invalid event performance entry, results in negative points ({points})")

    return int(points)


"""

LOADING PARAMETER TABLES

"""

def load_params(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, skipinitialspace=True) # reads in the text file as a csv (comma-separated values)
    df.columns = [column.strip().lower() for column in df.columns] # 
    df.set_index("event")
    return df


"""

Selecting correct table, for ease of use

"""

def _get_table(multievent: str, dec_df: pd.DataFrame, hep_df: pd.DataFrame) -> pd.DataFrame:
    
    multievent = multievent.lower()

    if multievent.startswith("dec"):
        return dec_df
    elif multievent.startswith("hep"):
        return hep_df
    else:
        raise ValueError(f"Unknown multievent type: {multievent}")