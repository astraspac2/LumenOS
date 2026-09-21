import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "core" / "users.json"


class Auth:
    def __init__(self):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    @property
    def current_user(self):
        return self.data["users"][0]

    def verify(self, password: str) -> bool:
        return password == self.current_user["password"]