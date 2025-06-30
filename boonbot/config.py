import json
import os

CONFIG_FILE = "./config.json"

class Config:
    guild_id: int = -1
    bot_channel_id: int = -1
    admin_role_id: int = -1
    team_names: list[str] = []
    contests_category_ids: list[int] = []
    team_role_ids: list[int] = []

    def save_to_file(self):
        config_data = {
            "team_names": self.team_names,
            "contests_category_ids": self.contests_category_ids,
            "team_role_ids": self.team_role_ids
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

    def load_from_file(self):
        if not os.path.exists(CONFIG_FILE):
            return False
        try:
            with open(CONFIG_FILE, "r") as f:
                config_data = json.load(f)
            self.team_names = config_data.get("team_names")
            self.contests_category_ids = config_data.get("contests_category_ids")
            self.team_role_ids = config_data.get("team_role_ids")
            return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False


config = Config()
