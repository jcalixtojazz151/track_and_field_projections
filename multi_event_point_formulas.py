import numpy as np

"""

FORMAT
track (running) events: seconds
field (jumping) events: centimeters
field (throwing) events: meters

"""

def track_event_points(event_time, a, b, c):
    points = a * (b - event_time) ** c
    return points.astype(int)

def field_event_points(event_distance, a, b, c):
    points = a * (event_distance - b) ** c
    return points.astype(int)