from pydantic import BaseModel, Field
from typing import Literal

# Status values matched from the frontend and Stage 1 contract
StatusEnum = Literal["online", "idle", "alert", "breach"]

class TelemetryPayload(BaseModel):
    assetId: str = Field(..., min_length=1, description="Unique identifier for the asset")
    name: str = Field(..., description="Human readable name of the asset")
    category: str = Field(..., description="Category like Electronics or Equipment")
    lat: float = Field(..., ge=-90.0, le=90.0, description="Latitude coordinate")
    lng: float = Field(..., ge=-180.0, le=180.0, description="Longitude coordinate")
    battery: float = Field(..., ge=0.0, le=100.0, description="Battery percentage remaining")
    status: StatusEnum = Field(..., description="Current status of the asset")
    gatewayId: str = Field(..., min_length=1, description="Identifier of the associated gateway")
    rssi: float = Field(..., ge=-150.0, le=0.0, description="Signal strength in dBm")
    timestamp: int = Field(..., gt=0, description="Unix timestamp of the telemetry reading")
