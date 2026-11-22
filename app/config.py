import os

from dotenv import load_dotenv

load_dotenv()

KEITARO_URL = os.getenv("KEITARO_URL", "")
KEITARO_KEY = os.getenv("KEITARO_KEY", "")