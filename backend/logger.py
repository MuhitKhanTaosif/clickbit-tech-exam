# logger.py
import logging

logger = logging.getLogger("ecommerce-backend")
logger.setLevel(logging.INFO)

# Stream handler
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
