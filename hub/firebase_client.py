import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

import config

logger = logging.getLogger("hub.firebase")

class FirebaseClient:
    def __init__(self):
        self.initialized = False
        
        if not config.FIREBASE_CREDENTIALS_PATH or not config.FIREBASE_DATABASE_URL:
            logger.warning("Firebase credentials or database URL not configured. Writes will be skipped.")
            return
            
        try:
            cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': config.FIREBASE_DATABASE_URL
            })
            self.initialized = True
            logger.info("Firebase initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")

    def update_node(self, path: str, data: dict, max_retries: int = 3):
        """
        Performs a partial update to the specified node with basic retry logic.
        """
        if not self.initialized:
            logger.debug(f"[Mock] Would write to Firebase -> {path}: {data}")
            return True

        for attempt in range(1, max_retries + 1):
            try:
                ref = db.reference(path)
                ref.update(data)
                return True
            except Exception as e:
                logger.error(f"Failed to update Firebase {path} on attempt {attempt}: {e}")
                if attempt < max_retries:
                    time.sleep(1) # simple backoff
                else:
                    logger.error(f"Max retries reached for Firebase update at {path}.")
                    return False

    def update_asset(self, asset_id: str, data: dict):
        """Update the asset using a partial update to preserve existing fields."""
        path = f"assets/{asset_id}"
        return self.update_node(path, data)

    def update_gateway(self, gateway_id: str, data: dict):
        """Update the gateway using a partial update to preserve existing fields."""
        path = f"gateways/{gateway_id}"
        return self.update_node(path, data)
