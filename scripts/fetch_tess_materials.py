#!/usr/bin/env python3
import json
from pathlib import Path
import requests
import sys

url = "https://tess.elixir-europe.org/materials"
headers = {
    "Accept": "application/vnd.api+json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
}
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Always save raw response and status for artifact inspection.
(output_dir / "status.txt").write_text(f"{response.status_code}\n", encoding="utf-8")
(output_dir / "response.txt").write_text(response.text, encoding="utf-8")

try:
    data = response.json()
    print("Successfully parsed JSON")
except requests.exceptions.JSONDecodeError as e:
    (output_dir / "json_decode_error.txt").write_text(str(e), encoding="utf-8")
    print(f"Error: Failed to parse JSON - {e}")
    print(f"Response: {response.text[:1000]}")
    sys.exit(1)

if response.status_code != 200:
    print("Error: Non-200 response")
    sys.exit(1)
