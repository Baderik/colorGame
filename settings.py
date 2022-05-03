from pathlib import Path

# DIRS
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "template"
STATIC_DIR = BASE_DIR / "static"
STATIC_URL = "/static/"

# Request/Response types
REQUEST_TYPES = ("changePartner", "changeColor")
RESPONSE_TYPES = ("start", "changePartner", "changeColor",
                  "disconnectPartner", "online", "message")
