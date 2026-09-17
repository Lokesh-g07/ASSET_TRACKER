import pytest
import sys
import os
import json
from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mqtt_handler import MqttSubscriber
from models import TelemetryPayload

@pytest.fixture
def mock_processor():
    return MagicMock()

def test_mqtt_valid_message(mock_processor):
    subscriber = MqttSubscriber(mock_processor)
    
    valid_json = json.dumps({
        "assetId": "AST-001",
        "name": "Asset-001",
        "category": "Electronics",
        "lat": 11.0,
        "lng": 76.0,
        "battery": 87.2,
        "status": "online",
        "gatewayId": "GW-03",
        "rssi": -65.4,
        "timestamp": 12345
    })
    
    mock_msg = MagicMock()
    mock_msg.topic = "asset/AST-001/telemetry"
    mock_msg.payload = valid_json.encode('utf-8')
    
    subscriber._on_message(None, None, mock_msg)
    
    # Verify processor was called with a parsed TelemetryPayload object
    mock_processor.process.assert_called_once()
    called_arg = mock_processor.process.call_args[0][0]
    assert isinstance(called_arg, TelemetryPayload)
    assert called_arg.assetId == "AST-001"

def test_mqtt_invalid_json(mock_processor):
    subscriber = MqttSubscriber(mock_processor)
    
    mock_msg = MagicMock()
    mock_msg.topic = "asset/AST-001/telemetry"
    mock_msg.payload = b"{invalid"
    
    # Should not raise exception
    subscriber._on_message(None, None, mock_msg)
    
    # Processor should not be called
    mock_processor.process.assert_not_called()

def test_mqtt_validation_error(mock_processor):
    subscriber = MqttSubscriber(mock_processor)
    
    invalid_json = json.dumps({
        "assetId": "AST-001",
        "battery": 150.0 # Missing fields and invalid battery
    })
    
    mock_msg = MagicMock()
    mock_msg.topic = "asset/AST-001/telemetry"
    mock_msg.payload = invalid_json.encode('utf-8')
    
    # Should not raise exception (caught internally)
    subscriber._on_message(None, None, mock_msg)
    
    # Processor should not be called
    mock_processor.process.assert_not_called()
