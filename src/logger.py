import logging
import os

# Create logs directory if it doesn't exist
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Logger setup complete.")