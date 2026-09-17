import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from firebase_client import FirebaseClient
from processor import TelemetryProcessor
from mqtt_handler import MqttSubscriber

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("hub.main")

# Global instances
firebase_client = None
processor = None
mqtt_subscriber = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing FastAPI Hub...")
    
    global firebase_client, processor, mqtt_subscriber
    
    firebase_client = FirebaseClient()
    processor = TelemetryProcessor(firebase_client)
    mqtt_subscriber = MqttSubscriber(processor)
    
    # Start the background MQTT client
    mqtt_subscriber.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI Hub...")
    if mqtt_subscriber:
        mqtt_subscriber.stop()

app = FastAPI(title="Campus Asset Tracker - Hub", lifespan=lifespan)

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    mqtt_status = "connected" if mqtt_subscriber and mqtt_subscriber.connected else "disconnected"
    firebase_status = "initialized" if firebase_client and firebase_client.initialized else "unconfigured"
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "mqtt": mqtt_status,
            "firebase": firebase_status
        }
    )
