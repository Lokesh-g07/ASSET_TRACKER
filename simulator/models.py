import time
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Location:
    lat: float
    lng: float

@dataclass
class Asset:
    asset_id: str
    name: str
    category: str
    location: Location
    battery: float
    status: str
    waypoints: List[Location] = field(default_factory=list)
    current_waypoint_index: int = 0

@dataclass
class Gateway:
    gateway_id: str
    name: str
    location: Location
    zone: str
    status: str = "online"
    
@dataclass
class Telemetry:
    asset_id: str
    name: str
    category: str
    lat: float
    lng: float
    battery: float
    status: str
    gateway_id: str
    rssi: float
    timestamp: int = field(default_factory=lambda: int(time.time()))

    def to_dict(self) -> dict:
        return {
            "assetId": self.asset_id,
            "name": self.name,
            "category": self.category,
            "lat": round(self.lat, 6),
            "lng": round(self.lng, 6),
            "battery": round(self.battery, 1),
            "status": self.status,
            "gatewayId": self.gateway_id,
            "rssi": round(self.rssi, 1),
            "timestamp": self.timestamp
        }
