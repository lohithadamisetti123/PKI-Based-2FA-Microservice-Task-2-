import requests
from pathlib import Path

# URL of your running 2FA microservice
API_URL = "http://localhost:8080/generate-2fa"

# Path to store the last code
LAST_CODE_FILE = Path("/cron/last_code.txt")

def fetch_2fa_code():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        code = data.get("code")
        return code
    except Exception as e:
        print(f"Error fetching 2FA code: {e}")
        return None

def save_code(code: str):
    try:
        LAST_CODE_FILE.write_text(code)
        print(f"Saved 2FA code: {code}")
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    code = fetch_2fa_code()
    if code:
        save_code(code)
