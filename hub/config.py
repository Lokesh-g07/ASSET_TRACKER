import os
from typing import Dict

# MQTT Configuration
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "asset/+/telemetry")
MQTT_QOS = int(os.getenv("MQTT_QOS", "1"))

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")

# Deduplication Configuration
DEDUP_CACHE_MAX_SIZE = int(os.getenv("DEDUP_CACHE_MAX_SIZE", "1000"))

# Provisional Location Mapping
# Note: This is a temporary approximation. In the future, the asset's true coordinates 
# should be used by a geofence engine to determine its actual zone.
GATEWAY_ZONE_MAPPING: Dict[str, str] = {
    "GW-01": "Eng Block",
    "GW-02": "Engineering Block",
    "GW-03": "Library",
    "GW-04": "Labs",
    "GW-05": "Admin",
    "GW-07": "Admin",
    "GW-09": "Main Hall",
    "GW-11": "Labs",
}
DEFAULT_ZONE = "Unknown Zone"
