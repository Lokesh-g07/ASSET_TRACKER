from typing import List, Tuple
from models import Asset, Gateway, Telemetry
from utils import haversine_distance, calculate_rssi

def generate_telemetry(asset: Asset, gateways: List[Gateway]) -> Telemetry:
    """
    Simulate the BLE discovery process.
    Finds the gateway with the strongest RSSI for the given asset.
    Returns a Telemetry object.
    """
    best_gateway = None
    best_rssi = -float('inf')
    
    # Calculate RSSI for all gateways to find the strongest signal
    for gw in gateways:
        if gw.status != "online":
            continue
            
        dist = haversine_distance(asset.location, gw.location)
        rssi = calculate_rssi(dist)
        
        if rssi > best_rssi:
            best_rssi = rssi
            best_gateway = gw
            
    # Fallback if no gateways are online (shouldn't happen in our basic sim)
    if not best_gateway:
        # Use a dummy values or just the first gateway
        best_gateway = gateways[0] if gateways else Gateway("GW-UNKNOWN", "Unknown", asset.location, "Unknown")
        best_rssi = -100.0

    return Telemetry(
        asset_id=asset.asset_id,
        name=asset.name,
        category=asset.category,
        lat=asset.location.lat,
        lng=asset.location.lng,
        battery=asset.battery,
        status=asset.status,
        gateway_id=best_gateway.gateway_id,
        rssi=best_rssi
    )
