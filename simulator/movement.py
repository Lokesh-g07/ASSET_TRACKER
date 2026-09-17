import random
from models import Asset, Location
from utils import move_towards
from config import MOVEMENT_SPEED_MPS, BATTERY_DRAIN_PER_TICK

def update_asset_position(asset: Asset, dt_seconds: float) -> None:
    """
    Update the position of the asset towards its current waypoint based on time delta.
    Also manages cycling to the next waypoint when reached.
    """
    if not asset.waypoints:
        return
        
    target_waypoint = asset.waypoints[asset.current_waypoint_index]
    
    # Calculate how far the asset can move in this tick
    distance_to_move = MOVEMENT_SPEED_MPS * dt_seconds
    
    # Move towards the waypoint
    asset.location = move_towards(asset.location, target_waypoint, distance_to_move)
    
    # Check if we reached the waypoint
    if asset.location.lat == target_waypoint.lat and asset.location.lng == target_waypoint.lng:
        # Cycle to next waypoint
        asset.current_waypoint_index = (asset.current_waypoint_index + 1) % len(asset.waypoints)

def drain_battery(asset: Asset) -> None:
    """
    Gradually decrease the asset's battery.
    """
    asset.battery -= BATTERY_DRAIN_PER_TICK
    # Optional slight variation to make it look realistic
    asset.battery -= random.uniform(0.0, 0.02)
    
    # Floor at 0
    if asset.battery < 0.0:
        asset.battery = 0.0

def update_asset(asset: Asset, dt_seconds: float) -> None:
    """
    Main update function for an asset for a given simulation tick.
    """
    update_asset_position(asset, dt_seconds)
    drain_battery(asset)
    
    # Basic status update (e.g. idle if battery is 0, else online)
    if asset.battery <= 0.0:
        asset.status = "idle"
    else:
        asset.status = "online"
