import pytest
import math
import sys
import os

# Add simulator dir to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Location, Asset, Gateway, Telemetry
from utils import haversine_distance, calculate_rssi, move_towards
from movement import update_asset_position, drain_battery
from ble import generate_telemetry
import config

def test_haversine_distance():
    # 1 degree of latitude is roughly 111km
    loc1 = Location(lat=0.0, lng=0.0)
    loc2 = Location(lat=1.0, lng=0.0)
    dist = haversine_distance(loc1, loc2)
    assert 110000 < dist < 112000

    # Same point should be 0
    assert haversine_distance(loc1, loc1) == 0.0

def test_calculate_rssi():
    # Test without noise to ensure deterministic behavior
    rssi_1m = calculate_rssi(1.0, apply_noise=False)
    assert rssi_1m == config.RSSI_AT_1M
    
    # RSSI should decrease as distance increases
    rssi_10m = calculate_rssi(10.0, apply_noise=False)
    assert rssi_10m < rssi_1m
    
    # Distance < 1m should cap at 1m to avoid positive log scaling
    rssi_0_5m = calculate_rssi(0.5, apply_noise=False)
    assert rssi_0_5m == config.RSSI_AT_1M
    
def test_move_towards():
    start = Location(lat=10.0, lng=10.0)
    target = Location(lat=10.1, lng=10.0)
    
    # Move a very small distance, should not reach target
    new_loc = move_towards(start, target, 1.0) # 1 meter
    assert new_loc.lat > 10.0
    assert new_loc.lat < 10.1
    
    # Move a massive distance, should cap at target
    new_loc_far = move_towards(start, target, 200000.0)
    assert new_loc_far.lat == 10.1
    assert new_loc_far.lng == 10.0

def test_battery_drain():
    asset = Asset(
        asset_id="1", name="test", category="test",
        location=Location(0,0), battery=10.0, status="online"
    )
    
    initial_battery = asset.battery
    drain_battery(asset)
    assert asset.battery < initial_battery
    
    # Ensure it doesn't go below 0
    asset.battery = 0.01
    drain_battery(asset)
    assert asset.battery == 0.0

def test_gateway_selection():
    asset = Asset(
        asset_id="1", name="test", category="test",
        location=Location(0,0), battery=100.0, status="online"
    )
    
    gw_far = Gateway(gateway_id="GW-FAR", name="Far", location=Location(1.0, 1.0), zone="A")
    gw_near = Gateway(gateway_id="GW-NEAR", name="Near", location=Location(0.001, 0.001), zone="B")
    gw_offline = Gateway(gateway_id="GW-OFF", name="Off", location=Location(0, 0), zone="C", status="offline")
    
    # Ensure random noise doesn't break this by running without it (mocking or relying on massive distance diff)
    # The distance diff is huge so noise won't affect it
    telemetry = generate_telemetry(asset, [gw_far, gw_near, gw_offline])
    
    # Should select near gateway
    assert telemetry.gateway_id == "GW-NEAR"
    assert telemetry.rssi > -100.0
    assert telemetry.status == "online"
    
def test_telemetry_serialization():
    t = Telemetry(
        asset_id="AST-1", name="A1", category="C1",
        lat=1.234567, lng=2.345678, battery=99.9,
        status="online", gateway_id="GW-1", rssi=-55.5
    )
    
    d = t.to_dict()
    assert d["assetId"] == "AST-1"
    assert d["lat"] == 1.234567
    assert "timestamp" in d
