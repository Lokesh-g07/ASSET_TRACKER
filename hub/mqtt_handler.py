import json
import logging
from pydantic import ValidationError
import paho.mqtt.client as mqtt

import config
from models import TelemetryPayload
from processor import TelemetryProcessor

logger = logging.getLogger("hub.mqtt")

class MqttSubscriber:
    def __init__(self, processor: TelemetryProcessor):
        self.processor = processor
        self.connected = False
        
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        except AttributeError:
            self.client = mqtt.Client()
            
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def start(self):
        try:
            logger.info(f"Connecting to MQTT broker at {config.MQTT_HOST}:{config.MQTT_PORT}...")
            self.client.connect(config.MQTT_HOST, config.MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT Connection failed on startup: {e}")
            self.connected = False

    def stop(self):
        logger.info("Stopping MQTT subscriber...")
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            self.connected = True
            logger.info(f"Connected to MQTT broker. Subscribing to {config.MQTT_TOPIC} (QoS {config.MQTT_QOS})")
            client.subscribe(config.MQTT_TOPIC, qos=config.MQTT_QOS)
        else:
            logger.error(f"Failed to connect to MQTT broker with reason code {reason_code}")

    def _on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties=None):
        self.connected = False
        logger.warning(f"Disconnected from MQTT broker (reason code {reason_code})")

    def _on_message(self, client, userdata, msg):
        try:
            # Parse JSON
            payload_dict = json.loads(msg.payload.decode('utf-8'))
            
            # Validate via Pydantic
            telemetry = TelemetryPayload(**payload_dict)
            
            # Pass to processor
            self.processor.process(telemetry)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Malformed JSON received on {msg.topic}: {e}")
        except ValidationError as e:
            logger.warning(f"Validation failed for payload on {msg.topic}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing message on {msg.topic}: {e}")
