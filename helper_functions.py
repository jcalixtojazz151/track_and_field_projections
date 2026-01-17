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


"""

def track_event_points(multievent: str, event: str, event_time: float, a: float, b: float, c: float) -> int:

    base = b - event_time

    if base <= 0:
        return 0
    
    points = a * base ** c
    
    return int(points)
        



def field_event_points(multievent: str, event: str, event_distance: float, a: float, b: float, c:float) -> int:

    base = event_distance - b

    if base <= 0:
        return 0

    points = a * base ** c

    return int(points)


"""

LOADING PARAMETER TABLES

"""

def load_params(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, skipinitialspace=True) # reads in the text file as a csv (comma-separated values)
    df.columns = [column.strip().lower() for column in df.columns]
    # df = df.set_index("event")
    return df

"""

Selecting correct table, for ease of use

"""

# def get_table(multievent: str, dec_df: pd.DataFrame, hep_df: pd.DataFrame) -> pd.DataFrame:
    
#     multievent = multievent.lower().strip()

#     if multievent.startswith("dec"):
#         return dec_df
#     elif multievent.startswith("hep"):
#         return hep_df
#     else:
#         raise ValueError(f"Unknown multievent type: {multievent}. Use decathlon or heptathlon.")


"""
Checks if its a float
"""

def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


"""
Checks if string has any digits
"""

def has_digits(s: str) -> bool:
    for char in s:
        if char.isdigit():
            return True
    
    return False

"""

To parse through results which use commas instead of decimals (55,55 cm instead of 55.55 cm). We want to standardize
all the data that comes in and this function helps us to convert everything to decimals.

"""

def normalize_decimal_separators(result: str) -> str:

    # Otherwise, the number has some additional content. First, we remove all space before and after 
    result.strip()

    # Replace comma used as decimal separator (7,80 -> 7.80)
    if ',' in result:
        result = result.replace(',', '.')

    return result


"""

"""


def parse_time_to_seconds(result: str) -> str:

    type_of_measurement = ""

    # First normalize commas to decimals
    result = normalize_decimal_separators(result)

    # Then, remove all space before and after and put everything in lowercase
    result_string = result.lower()

    # If the athlete obtained a result, there are many cases to consider:

    # Remove all spaces in the text (5m 55.55s -> 5m55.55s)
    result_string_no_spaces = result_string.replace(" ", "")

    # Check whether there is a letter at the end of the string (h or s)

    if is_float(result_string_no_spaces):

        if "." not in result_string_no_spaces:
            result_string_no_spaces += ".0h"
            return result_string_no_spaces
        
        else:
            number_of_decimal_places = len(result_string_no_spaces.split(".")[1])

            if number_of_decimal_places == 0:
                result_string_no_spaces += "0h"
                return result_string_no_spaces
            elif number_of_decimal_places == 1:
                result_string_no_spaces += "h"
                return result_string_no_spaces
            elif number_of_decimal_places >= 3:

                decimal_position = result_string_no_spaces.find(".")

                result_for_calculation = result_string_no_spaces[:decimal_position+2]
                extra_digits = result_string_no_spaces[decimal_position+2:]
                if int(extra_digits) > 0:
                    result_for_calculation = str(float(result_for_calculation) + 0.01)
                
                number_of_decimal_places = len(result_for_calculation.split(".")[1])

                if number_of_decimal_places == 1:
                    result_for_calculation += "0"
                    return result_for_calculation
                    




    # Case 1: colon form (5:55.55)
    if ":" in result_string:
        minutes_string, seconds_string = result_string.split(":", maxsplit=1)
        minutes = float(minutes_string)
        seconds = float(seconds_string)
        return minutes * 60 + seconds
    
    # Case 2: '5m55.55s' (with or without space originally)
    if "m" in result_string_no_spaces and result_string_no_spaces.endswith("s"):
        minutes_string, seconds_string_with_s = result_string_no_spaces.split("m", maxsplit = 1)
        seconds_string = seconds_string_with_s[:-1] # drop trailing "s"
        minutes = float(minutes_string)
        seconds = float(seconds_string)
        return minutes * 60 + seconds


    # If the athlete did not obtain a numeric result, they get 0 points and a descriptor of the result (dq, dnf, dns, etc.)

    if has_digits(result_string) == False:
        return result_string



# Create a function that cleans the float for seconds to be reused when dealing with minutes. Clean up the way the function works itself - too many if statements. Perhaps there is a better way to do it.


