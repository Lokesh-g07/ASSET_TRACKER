import math
import random
from models import Location
from config import RSSI_AT_1M, PATH_LOSS_EXPONENT, NOISE_STD_DEV

def haversine_distance(loc1: Location, loc2: Location) -> float:
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees).
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [loc1.lng, loc1.lat, loc2.lng, loc2.lat])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 # Radius of earth in meters
    return c * r

def calculate_rssi(distance: float, apply_noise: bool = True) -> float:
    """
    Calculate approximated RSSI using a log-distance path loss model.
    RSSI(d) = RSSI_0 - 10 * n * log10(d / d_0) + noise
    where d_0 is 1 meter.
    """
    if distance < 1.0:
        distance = 1.0  # Cap minimum distance to 1m to avoid positive log values
        
    rssi = RSSI_AT_1M - 10 * PATH_LOSS_EXPONENT * math.log10(distance)
    
    if apply_noise:
        noise = random.gauss(0, NOISE_STD_DEV)
        rssi += noise
        
    # Bound the RSSI to sensible BLE limits
    return max(-100.0, min(-20.0, rssi))

def move_towards(current: Location, target: Location, distance_meters: float) -> Location:
    """
    Calculate a new location by moving from `current` towards `target` by `distance_meters`.
    """
    total_dist = haversine_distance(current, target)
    if total_dist <= distance_meters:
        # We will reach or overshoot the target this tick
        return Location(lat=target.lat, lng=target.lng)
        
    # Simple linear interpolation (sufficient for small campus distances)
    ratio = distance_meters / total_dist
    new_lat = current.lat + (target.lat - current.lat) * ratio
    new_lng = current.lng + (target.lng - current.lng) * ratio
    return Location(lat=new_lat, lng=new_lng)
