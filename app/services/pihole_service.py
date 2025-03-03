import json
import os
import time

import requests

from app.config import Config

SESSION_FILE = "/home/cali/projects/VitaSync/session/pihole_session.json"


def load_session():
    """Load stored session from a file if it exists and is valid."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            session_data = json.load(f)
            sid = session_data.get("sid")
            timestamp = session_data.get("timestamp", 0)

            if time.time() - timestamp < 1800:
                return sid

    return None


def save_session(sid):
    """Save the session to a file with a timestamp."""
    with open(SESSION_FILE, "w") as f:
        json.dump({"sid": sid, "timestamp": time.time()}, f)


def authenticate():
    """Authenticate to Pi-hole and return a session ID (SID)."""
    sid = load_session()
    if sid:
        return sid

    auth_url = f"{Config.PIHOLE_URL}/api/auth"
    headers = {"Content-Type": "application/json"}
    payload = {"password": Config.PIHOLE_PASSWORD}

    try:
        response = requests.post(
            auth_url, headers=headers, data=json.dumps(payload), verify=False
        )
        response.raise_for_status()
        data = response.json()

        if data.get("session", {}).get("valid"):
            sid = data["session"].get("sid")
            save_session(sid)
            return sid
        else:
            print("Authentication failed: Invalid session.")
    except requests.exceptions.RequestException as e:
        print(f"Authentication request failed: {e}")

    return None


def get_pihole_stats():
    """Fetch Pi-hole stats using the stored SID."""
    sid = authenticate()
    if not sid:
        return {"ERROR": "Authentication failed."}

    stats_url = f"{Config.PIHOLE_URL}/api/stats/summary"
    headers = {"accept": "application/json", "sid": sid}

    try:
        response = requests.get(stats_url, headers=headers, verify=False)
        response.raise_for_status()
        data = response.json()

        return {
            "data": {
                "dns_queries_today": data["queries"]["total"],
                "ads_blocked_today": data["queries"]["blocked"],
                "ads_percentage_today": data["queries"]["percent_blocked"],
                "domains_being_blocked": data["gravity"]["domains_being_blocked"],
                "unique_domains": data["queries"]["unique_domains"],
                "unique_clients": data["clients"]["active"],
            }
        }

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve Pi-hole stats: {e}")
        return {"ERROR": "Something went wrong gathering data."}
