import pytest
import json
import os
import sys
from unittest.mock import MagicMock, patch

# Add simulator dir to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from models import Telemetry

# We must patch config before importing MqttPublisher
# but since it's already imported, we can mock the class behavior directly
from mqtt_client import MqttPublisher
import paho.mqtt.client as mqtt

@pytest.fixture
def mock_telemetry():
    return Telemetry(
        asset_id="AST-001",
        name="TestAsset",
        category="Test",
        lat=11.1,
        lng=76.1,
        battery=100.0,
        status="online",
        gateway_id="GW-01",
        rssi=-50.0
    )

@patch("mqtt_client.mqtt.Client")
def test_mqtt_disabled_does_not_connect(mock_client_class):
    # Ensure it's disabled
    config.MQTT_ENABLED = False
    
    pub = MqttPublisher()
    
    # Client should not be created
    assert pub.client is None
    assert pub.connected is False
    assert pub.get_status_string() == "Disabled"
    
    # Publish should silently do nothing
    pub.publish([MagicMock()])
    mock_client_class.return_value.publish.assert_not_called()


@patch("mqtt_client.mqtt.Client")
def test_mqtt_enabled_connects(mock_client_class, mock_telemetry):
    config.MQTT_ENABLED = True
    config.MQTT_HOST = "localhost"
    config.MQTT_PORT = 1883
    config.MQTT_QOS = 1
    
    mock_client_instance = mock_client_class.return_value
    
    pub = MqttPublisher()
    
    # Should attempt to connect and start loop
    mock_client_instance.connect.assert_called_once_with("localhost", 1883, keepalive=60)
    mock_client_instance.loop_start.assert_called_once()
    
    # Simulate successful connection callback
    pub._on_connect(mock_client_instance, None, None, 0)
    assert pub.connected is True
    assert pub.get_status_string() == "Connected"
    
    # Test publishing
    mock_msg_info = MagicMock()
    mock_msg_info.rc = mqtt.MQTT_ERR_SUCCESS
    mock_client_instance.publish.return_value = mock_msg_info
    
    pub.publish([mock_telemetry])
    
    expected_topic = "asset/AST-001/telemetry"
    expected_payload = json.dumps(mock_telemetry.to_dict())
    
    mock_client_instance.publish.assert_called_once_with(
        expected_topic,
        expected_payload,
        qos=1,
        retain=False
    )
    
    # Stop should cleanup
    pub.stop()
    mock_client_instance.loop_stop.assert_called_once()
    mock_client_instance.disconnect.assert_called_once()
