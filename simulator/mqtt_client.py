import json
import paho.mqtt.client as mqtt
from typing import List
from models import Telemetry
import config

class MqttPublisher:
    def __init__(self):
        self.enabled = config.MQTT_ENABLED
        self.connected = False
        self.client = None

        if self.enabled:
            # Setup MQTT client
            # Using API v2 if paho-mqtt >= 2.0.0
            try:
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            except AttributeError:
                # Fallback for older paho-mqtt versions
                self.client = mqtt.Client()
                
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            
            # Start connection
            self.connect()

    def connect(self):
        if not self.enabled or not self.client:
            return

        try:
            # We connect without blocking the main thread entirely, 
            # and start the network loop in the background.
            self.client.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            # Graceful failure: don't crash if broker is down.
            # We just won't be marked as connected, and loop_start() will handle retries 
            # if we managed to at least initialize, though immediate connect() fails might need 
            # manual handling depending on the OS. But paho handles background reconnects well.
            self.connected = False
            # We log this gracefully without breaking the UI
            pass 

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            self.connected = True

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties=None):
        self.connected = False

    def get_status_string(self) -> str:
        if not self.enabled:
            return "Disabled"
        return "Connected" if self.connected else "Broker Unavailable"

    def publish(self, telemetry_list: List[Telemetry]):
        """Publish a list of telemetry events to their respective topics."""
        if not self.enabled or not self.client or not self.connected:
            return

        for t in telemetry_list:
            topic = f"asset/{t.asset_id}/telemetry"
            payload = json.dumps(t.to_dict())
            
            # QoS 1 is chosen to ensure at-least-once delivery for telemetry,
            # which is suitable for eventual ingestion by the FastAPI Hub.
            # Retain is False because telemetry is a stream of events, not persistent static state.
            msg_info = self.client.publish(
                topic, 
                payload, 
                qos=config.MQTT_QOS, 
                retain=False
            )
            
            # We don't block on wait_for_publish() to keep the async simulation loop fast,
            # but in a stricter environment we could inspect msg_info.rc to verify successful queueing.
            if msg_info.rc != mqtt.MQTT_ERR_SUCCESS:
                # Could log a localized warning here if needed
                pass

    def stop(self):
        """Cleanly disconnect and stop the MQTT background thread."""
        if self.enabled and self.client:
            self.client.loop_stop()
            self.client.disconnect()
