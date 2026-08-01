import os


A2A_VERSION = "1.0"


API_TOKEN = os.getenv(
    "API_TOKEN",
    "secret123"
)


DATABASE_URL = (
    "sqlite:///./invoice.db"
)