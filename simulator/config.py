"""
Configuration parameters for the Campus Asset Tracker IoT Simulator.
"""

# Simulation constraints
SIMULATION_INTERVAL_SEC = 2.0  # How often the simulation updates
MOVEMENT_SPEED_MPS = 1.5       # Meters per second (approx walking speed)
BATTERY_DRAIN_PER_TICK = 0.05  # Percentage of battery drained per tick
RANDOM_SEED = 42               # Set for deterministic tests, or None for random

# MQTT Configuration
import os
MQTT_ENABLED = os.getenv("MQTT_ENABLED", "false").lower() == "true"
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_QOS = int(os.getenv("MQTT_QOS", "1"))

# Geographic bounds for the campus simulation (approx 11.016 N, 76.955 E)
CAMPUS_BOUNDS = {
    "min_lat": 11.0150,
    "max_lat": 11.0180,
    "min_lng": 76.9540,
    "max_lng": 76.9570,
}

# Entity counts
NUM_ASSETS = 15
NUM_GATEWAYS = 5

# BLE log-distance path loss parameters
# Formula: RSSI(d) = RSSI_0 - 10 * n * log10(d / d_0) + noise
RSSI_AT_1M = -30.0             # RSSI_0: Expected signal strength at 1 meter (dBm)
PATH_LOSS_EXPONENT = 2.5       # n: Path-loss exponent (free space is 2, indoor office is 2 to 3)
NOISE_STD_DEV = 3.0            # Standard deviation for random Gaussian noise (dBm)

# Status choices
ASSET_STATUS_ONLINE = "online"
ASSET_STATUS_IDLE = "idle"

# Categories
ASSET_CATEGORIES = [
    "Electronics",
    "Equipment",
    "Machinery",
    "IT Equipment"
]
