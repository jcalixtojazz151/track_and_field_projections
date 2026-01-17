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

def track_event_points(event_time: float, parameter_row: pd.Series) -> int:
    """
    Docstring for track_event_points
    
    :param event_time: Description
    :type event_time: float
    :param parameter_row: Description
    :type parameter_row: pd.Series
    :return: Description
    :rtype: int
    """

    a = parameter_row["a"]
    b = parameter_row["b"]
    c = parameter_row["c"]

    base = b - event_time

    if base <= 0:
        return 0
    
    points = a * base ** c
    
    return int(points)
        



def field_event_points(event_distance: float, parameter_row: pd.Series) -> int:
    """
    Docstring for field_event_points
    
    :param event_distance: Description
    :type event_distance: float
    :param parameter_row: Description
    :type parameter_row: pd.Series
    :return: Description
    :rtype: int
    """
    
    a = parameter_row["a"]
    b = parameter_row["b"]
    c = parameter_row["c"]

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
    return df

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
    """
    Docstring for normalize_decimal_separators
    
    :param result: Description
    :type result: str
    :return: Description
    :rtype: str
    """

    # Otherwise, the number has some additional content. First, we remove all space before and after 
    clean_result = result.lower()

    # Replace comma used as decimal separator (7,80 -> 7.80)
    if ',' in clean_result:
        clean_result = clean_result.replace(',', '.')

    return clean_result


def clean_seconds_format(seconds_string: str) -> str:
    """
    Docstring for clean_seconds_format
    
    :param seconds: Description
    :type seconds: str
    :return: Description
    :rtype: str
    """

    # Check whether float is a integer (no following .)
    # We add a .0h to identify it as a manually marked time (by hand)
    if "." not in seconds_string:
        seconds_string += ".0h"
        return seconds_string
    
    else:

        # Extract the components of track result
        result_string_components = seconds_string.split(".")
        whole_seconds = result_string_components[0]
        decimal_seconds = result_string_components[1]
        number_of_decimal_places = len(decimal_seconds)
        
        # If there are no decimal places (i.e. 11.), we add "0h" to identify it as a manually marked time (by hand)
        if number_of_decimal_places == 0:
            seconds_string += "0h"
            return seconds_string
        
        # If there is 1 decimal place (i.e. 11.5), we add "h" to identify it as a manually marked time (by hand)
        elif number_of_decimal_places == 1:
            seconds_string += "h"
            return seconds_string
        
        elif number_of_decimal_places == 2:
            return seconds_string
        
        # If there is 2 or more decimal places (i.e. 11.36), 
        elif number_of_decimal_places >= 3:

            # Define the digits after 2 decimal places and the final result used for calculation (only up to 2 decimal places)
            extra_digits = decimal_seconds[2:]
            seconds_string_short = whole_seconds + "." + decimal_seconds[:2]

            # If the value of the extra digits is greater than 0, we need to add 1 centisecond to the final result
            if int(extra_digits) > 0:
                seconds_string_short = str(float(seconds_string_short) + 0.01)
            
            # In the case where the final result goes from 11.99 to 12.0, for example, we need to add another 0 to convert it to 12.00
            # This is to confirm that the time is not manually marked and is electronic
            if len(seconds_string_short.split(".")[1]) == 1:
                seconds_string_short += "0"
                return seconds_string_short
            
            return seconds_string_short



def parse_time_to_seconds(result: str) -> str:
    """
    Docstring for parse_time_to_seconds
    
    :param result: Description
    :type result: str
    :return: Description
    :rtype: str
    """
    
    # Remove all spaces in the text (5m 55.55s -> 5m55.55s)
    result_string_clean = result.replace(" ", "")

    # If the athlete did not obtain a numeric result, we return the same string that came in (i.e. "dq", "dnf", "dns", "nm", "")
    if has_digits(result_string_clean) == False:
        return result_string_clean


    # First normalize commas to decimals
    normalized_result_string = normalize_decimal_separators(result_string_clean)


    # If the athlete obtained a result, there are many cases to consider:

    # Check whether there is result is a float (i.e. 11, 11., 11.5, etc.) - no letters, only numbers and periods - and return the result in the
    # correct seconds format
    if is_float(normalized_result_string):

        return clean_seconds_format(seconds_string=normalized_result_string)
    

    # If the result string ends in h, it is a manual time and it requires slight manipulation to put it in the correct format
    if normalized_result_string[-1] == "h":

        if is_float(normalized_result_string[:-1]):

            manual_time_string = normalized_result_string[:-1]

            ### Figure out how to handle the h in the result (maybe modifying the helper function)

            manual_time_string_components = manual_time_string.split('.')
            whole_seconds = manual_time_string_components[0]
            decimal_seconds = manual_time_string_components[1]



    # If the result string ends in s, there is one case that is in seconds and easy to manage
    elif normalized_result_string[-1] == "s":

        if is_float(normalized_result_string[:-1]):

            return clean_seconds_format(seconds_string=normalized_result_string[:-1])



    # If the result string is not a float, it must include a letter, and there are multiple cases to check
    # Case 1: colon form (5:55.55)
    if ":" in result_string_clean:
        time_components = result_string_clean.split(":", maxsplit=1)
        minutes = float(minutes_string)
        seconds = clean_seconds_format(seconds_string=seconds_string)
        return minutes * 60 + seconds
    
    # Case 2: '5m55.55s' (with or without space originally)
    if "m" in result_string_clean and result_string_clean.endswith("s"):
        minutes_string, seconds_string_with_s = result_string_clean.split("m", maxsplit = 1)
        seconds_string = seconds_string_with_s[:-1] # drop trailing "s"
        minutes = float(minutes_string)
        seconds = float(seconds_string)
        return minutes * 60 + seconds


# Create a function that cleans the float for seconds to be reused when dealing with minutes. Clean up the way the function works itself - too many if statements. Perhaps there is a better way to do it.


