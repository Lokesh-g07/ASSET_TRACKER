import logging
from collections import OrderedDict
from datetime import datetime

from models import TelemetryPayload
from firebase_client import FirebaseClient
import config

logger = logging.getLogger("hub.processor")

class TelemetryProcessor:
    def __init__(self, firebase_client: FirebaseClient):
        self.firebase_client = firebase_client
        # Simple in-memory LRU cache for deduplication (assetId + timestamp)
        self.processed_ids = OrderedDict()
        self.max_cache_size = config.DEDUP_CACHE_MAX_SIZE

    def _is_duplicate(self, telemetry: TelemetryPayload) -> bool:
        """Check if we have already processed this exact telemetry event."""
        unique_id = f"{telemetry.assetId}_{telemetry.timestamp}"
        if unique_id in self.processed_ids:
            return True
            
        # Add to cache and maintain size limit
        self.processed_ids[unique_id] = True
        if len(self.processed_ids) > self.max_cache_size:
            self.processed_ids.popitem(last=False)
            
        return False

    def _derive_location(self, gateway_id: str) -> str:
        """
        Provisional approximation of the asset's location.
        Note: True location should eventually be determined by a geofence engine 
        using actual lat/lng coordinates, rather than relying solely on the gateway zone.
        """
        return config.GATEWAY_ZONE_MAPPING.get(gateway_id, config.DEFAULT_ZONE)

    def process(self, telemetry: TelemetryPayload) -> bool:
        """
        Converts validated telemetry into Firebase updates and executes them safely.
        Returns True if processed successfully (or safely skipped as duplicate).
        """
        if self._is_duplicate(telemetry):
            logger.debug(f"Duplicate telemetry skipped: {telemetry.assetId} at {telemetry.timestamp}")
            return True

        location_approx = self._derive_location(telemetry.gatewayId)

        # Asset Update Mapping
        asset_update = {
            "name": telemetry.name,
            "category": telemetry.category,
            "location": location_approx,
            "status": telemetry.status,
            "battery": round(telemetry.battery, 1),
            "lat": round(telemetry.lat, 6),
            "lng": round(telemetry.lng, 6),
            "gatewayId": telemetry.gatewayId,
            "rssi": round(telemetry.rssi, 1),
            "lastSeen": telemetry.timestamp
        }

        # Gateway Update Mapping
        gateway_update = {
            "rssi": round(telemetry.rssi, 1),
            "status": "online",
            # We preserve the actual timestamp, but can also format it if frontend expects it
            "lastPing": telemetry.timestamp 
        }

        # Perform the actual writes
        # If the write fails, we log it, but we already added the ID to the processed cache.
        # This keeps our failure handling simple without complex queues.
        asset_success = self.firebase_client.update_asset(telemetry.assetId, asset_update)
        gateway_success = self.firebase_client.update_gateway(telemetry.gatewayId, gateway_update)
        
        if asset_success and gateway_success:
            logger.info(f"Processed telemetry for {telemetry.assetId}")
            return True
        else:
            logger.error(f"Failed to process telemetry fully for {telemetry.assetId}")
            return False
