from dotenv import load_dotenv
import os

load_dotenv()

# JWT Configuration
access_token_expire_minuites = os.getenv("ACCESS_TOKEN_EXPIRE_MINUITES", "30")