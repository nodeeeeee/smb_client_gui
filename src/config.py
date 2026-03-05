import json
import os

CONFIG_FILE = os.path.expanduser("~/.smb_client_gui.json")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "credentials": [],
            "last_printer": "psts",
            "last_duplex": True
        }
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {
                "credentials": [],
                "last_printer": "psts",
                "last_duplex": True
            }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_credentials():
    config = load_config()
    return config.get("credentials", [])

def add_credential(username, password):
    config = load_config()
    credentials = config.get("credentials", [])
    # Check if username already exists, if so update it
    for cred in credentials:
        if cred["username"] == username:
            cred["password"] = password
            save_config(config)
            return
    credentials.append({"username": username, "password": password})
    config["credentials"] = credentials
    save_config(config)

def delete_credential(username):
    config = load_config()
    credentials = config.get("credentials", [])
    config["credentials"] = [cred for cred in credentials if cred["username"] != username]
    save_config(config)

def edit_credential(old_username, new_username, new_password):
    config = load_config()
    credentials = config.get("credentials", [])
    for cred in credentials:
        if cred["username"] == old_username:
            cred["username"] = new_username
            cred["password"] = new_password
            break
    config["credentials"] = credentials
    save_config(config)

def get_last_settings():
    config = load_config()
    return config.get("last_printer", "psts"), config.get("last_duplex", True)

def save_last_settings(printer, duplex):
    config = load_config()
    config["last_printer"] = printer
    config["last_duplex"] = duplex
    save_config(config)
