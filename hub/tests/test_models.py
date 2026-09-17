import pytest
from pydantic import ValidationError
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import TelemetryPayload

def test_valid_telemetry():
    data = {
        "assetId": "AST-001",
        "name": "Asset-001",
        "category": "Electronics",
        "lat": 11.016254,
        "lng": 76.955123,
        "battery": 87.2,
        "status": "online",
        "gatewayId": "GW-03",
        "rssi": -65.4,
        "timestamp": 1718029302
    }
    payload = TelemetryPayload(**data)
    assert payload.assetId == "AST-001"
    assert payload.battery == 87.2

def test_battery_validation_accepted():
    base_data = {
        "assetId": "AST-001", "name": "A", "category": "C",
        "lat": 11.0, "lng": 76.0, "status": "online",
        "gatewayId": "GW-01", "rssi": -50.0, "timestamp": 123
    }
    # Valid values
    for val in [0.0, 50.0, 100.0, 87.2]:
        base_data["battery"] = val
        payload = TelemetryPayload(**base_data)
        assert payload.battery == val

def test_battery_validation_rejected():
    base_data = {
        "assetId": "AST-001", "name": "A", "category": "C",
        "lat": 11.0, "lng": 76.0, "status": "online",
        "gatewayId": "GW-01", "rssi": -50.0, "timestamp": 123
    }
    # Invalid values
    for val in [-1.0, -5.0, 100.1, 150.0]:
        base_data["battery"] = val
        with pytest.raises(ValidationError):
            TelemetryPayload(**base_data)

def test_invalid_coordinates_rejected():
    data = {
        "assetId": "AST-001", "name": "A", "category": "C",
        "lat": 100.0, "lng": 76.0, "status": "online", # lat > 90
        "gatewayId": "GW-01", "rssi": -50.0, "timestamp": 123,
        "battery": 50.0
    }
    with pytest.raises(ValidationError):
        TelemetryPayload(**data)

def test_invalid_rssi_rejected():
    data = {
        "assetId": "AST-001", "name": "A", "category": "C",
        "lat": 11.0, "lng": 76.0, "status": "online", 
        "gatewayId": "GW-01", "rssi": 10.0, "timestamp": 123, # rssi > 0
        "battery": 50.0
    }
    with pytest.raises(ValidationError):
        TelemetryPayload(**data)

def test_invalid_status_rejected():
    data = {
        "assetId": "AST-001", "name": "A", "category": "C",
        "lat": 11.0, "lng": 76.0, "status": "exploding", # invalid status
        "gatewayId": "GW-01", "rssi": -50.0, "timestamp": 123, 
        "battery": 50.0
    }
    with pytest.raises(ValidationError):
        TelemetryPayload(**data)

def test_missing_field_rejected():
    data = {
        "assetId": "AST-001", "name": "A", "category": "C"
        # missing lots of fields
    }
    with pytest.raises(ValidationError):
        TelemetryPayload(**data)
