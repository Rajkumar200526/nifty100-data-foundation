import json
from pathlib import Path

from src.api.main import app

Path("docs").mkdir(exist_ok=True)

with open("docs/openapi.json", "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)

print("OpenAPI specification exported successfully.")