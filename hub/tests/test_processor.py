import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import TelemetryPayload
from processor import TelemetryProcessor
import config

@pytest.fixture
def valid_telemetry():
    return TelemetryPayload(
        assetId="AST-001",
        name="Asset-001",
        category="Electronics",
        lat=11.016254,
        lng=76.955123,
        battery=87.2,
        status="online",
        gatewayId="GW-03",
        rssi=-65.4,
        timestamp=1718029302
    )

def test_deduplication(valid_telemetry):
    mock_firebase = MagicMock()
    mock_firebase.update_asset.return_value = True
    mock_firebase.update_gateway.return_value = True
    
    processor = TelemetryProcessor(mock_firebase)
    
    # First process should work
    res1 = processor.process(valid_telemetry)
    assert res1 is True
    assert mock_firebase.update_asset.call_count == 1
    
    # Second process with same timestamp should be ignored
    res2 = processor.process(valid_telemetry)
    assert res2 is True # It returns True because it's safely handled
    assert mock_firebase.update_asset.call_count == 1 # Did not increment
    
    # Third process with new timestamp should work
    new_telemetry = valid_telemetry.model_copy(update={"timestamp": 1718029305})
    res3 = processor.process(new_telemetry)
    assert res3 is True
    assert mock_firebase.update_asset.call_count == 2

def test_data_transform(valid_telemetry):
    mock_firebase = MagicMock()
    processor = TelemetryProcessor(mock_firebase)
    
    # Force a known location mapping
    config.GATEWAY_ZONE_MAPPING["GW-03"] = "Test Library"
    
    processor.process(valid_telemetry)
    
    # Check asset update mapping
    mock_firebase.update_asset.assert_called_once()
    asset_args = mock_firebase.update_asset.call_args[0]
    assert asset_args[0] == "AST-001"
    
    asset_data = asset_args[1]
    assert asset_data["location"] == "Test Library"
    assert asset_data["battery"] == 87.2
    assert asset_data["gatewayId"] == "GW-03"
    assert asset_data["lastSeen"] == 1718029302
    
    # Check gateway update mapping
    mock_firebase.update_gateway.assert_called_once()
    gateway_args = mock_firebase.update_gateway.call_args[0]
    assert gateway_args[0] == "GW-03"
    
    gateway_data = gateway_args[1]
    assert gateway_data["status"] == "online"
    assert gateway_data["rssi"] == -65.4
    assert gateway_data["lastPing"] == 1718029302
