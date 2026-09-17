# Campus Asset Tracker - IoT Environment Simulator

This simulator represents the physical BLE/IoT environment for development and demonstration of the Campus Asset Tracker project. 

> **IMPORTANT:** This is a software simulation to generate realistic telemetry data. It is **not** a replacement for hardware validation using actual ESP32 devices and BLE tags.

## Purpose and Architecture Role

In the full architecture, BLE tags attached to assets broadcast signals that are picked up by ESP32 gateways, sent over LoRa to a Raspberry Pi hub, and ingested via MQTT.

This Python simulator replicates that physical layer (Stage 2). It runs independently, managing virtual assets, calculating simulated BLE RSSI (signal strength), and determining gateway associations as assets move around virtual waypoints.

## Architecture

```text
┌────────────────────┐
│ Python Simulator   │
│                    │
│ Movement           │
│ BLE/RSSI           │
│ Battery            │
└─────────┬──────────┘
          │
          │ MQTT (asset/{id}/telemetry)
          ↓
┌────────────────────┐
│ Mosquitto Broker   │
└─────────┬──────────┘
          │
          ↓
   Future Stage 4
   FastAPI Hub
```

> **Note:** The FastAPI Hub is **not implemented yet**. The simulator currently publishes telemetry to the MQTT broker, where it waits for future stages.

## How to Install

You will need Python 3 installed. We recommend using a virtual environment.

```bash
cd simulator
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

*(If you wish to run the tests, also install `pip install -r requirements-dev.txt`)*

## How to Run

```bash
# Ensure you are in the simulator directory with your venv activated
python main.py
```

You will see a live-updating table in your terminal showing all assets, their current locations, associated gateways, RSSI, battery, and status. Use `Ctrl+C` to stop the simulation.

## Configuration

All configuration is located in `config.py`. You can change:
- `MQTT_ENABLED`: Set to `True` (or environment variable `MQTT_ENABLED=true`) to publish to Mosquitto. Defaults to `False`.
- `MQTT_HOST`: Defaults to `localhost`.
- `MQTT_PORT`: Defaults to `1883`.
- `MQTT_QOS`: Defaults to `1` (At least once delivery). `retain` is hardcoded to `False` as telemetry is a stream.
- `SIMULATION_INTERVAL_SEC`: How often the simulation loop updates (seconds).
- `MOVEMENT_SPEED_MPS`: How fast assets move between waypoints (meters per second).
- `BATTERY_DRAIN_PER_TICK`: How much battery drains every interval.
- `CAMPUS_BOUNDS`: The geographic boundaries (latitude/longitude) where assets spawn.
- `NUM_ASSETS` and `NUM_GATEWAYS`.
- **RSSI Model parameters:** `RSSI_AT_1M`, `PATH_LOSS_EXPONENT`, `NOISE_STD_DEV`.

## Simulation Models

### Simulated Assets
Assets are spawned at random locations within the `CAMPUS_BOUNDS`. Each asset is given a set of 3-5 randomized waypoints. 

### Movement Model
Assets do not teleport or wander randomly. They use **scripted waypoint movement**. Every tick, the simulator calculates how far the asset can move based on `MOVEMENT_SPEED_MPS` and updates its latitude and longitude incrementally along a straight line (great circle route) toward its current waypoint using the Haversine formula. When a waypoint is reached, it cycles to the next one.

### Simulated Gateways
Gateways are placed randomly within the simulation bounds. They represent the stationary ESP32 receivers.

### RSSI Model
BLE signal strength is simulated using a **log-distance path-loss model**:
`RSSI(d) = RSSI_0 - 10 * n * log10(d / d_0) + noise`

Where:
- `RSSI_0` is the expected signal strength at 1 meter.
- `d` is the Haversine distance between the asset and the gateway.
- `n` is the path-loss exponent.
- `noise` is random Gaussian noise to simulate environmental variance.

Assets automatically associate with the gateway that provides the strongest RSSI. As assets move, their RSSI changes dynamically, resulting in natural gateway switching if their path crosses coverage boundaries.

## Testing

Basic mathematical and logic tests are provided via `pytest`.

```bash
pytest tests/
```

## MQTT Testing

To verify the MQTT transport:
1. Ensure Mosquitto is running locally (e.g., via Docker: `docker run -it -p 1883:1883 eclipse-mosquitto`).
2. Run the simulator with MQTT enabled:
   ```bash
   # On Windows PowerShell
   $env:MQTT_ENABLED="true"; python main.py
   ```
3. Subscribe to the topics in another terminal:
   ```bash
   mosquitto_sub -h localhost -t "asset/+/telemetry" -v
   ```
   You should see JSON payloads arriving every tick.

If the Mosquitto broker is unavailable, the simulator will log the status in the UI but will **not crash**. It will gracefully continue simulating movement while silently failing to publish.

## Current Limitations
- Geofence breach logic is not currently implemented. Assets will always report `online` or `idle` (if battery dies).
- The "Campus Bounds" are currently a simple bounding box without true geographical terrain awareness.
