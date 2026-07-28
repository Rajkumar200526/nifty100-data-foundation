import json
from src.api.main import app

with open("docs/openapi.json", "w", encoding="utf-8") as f:
    json.dump(app.openapi(), f, indent=2)

print("OpenAPI specification exported successfully.")