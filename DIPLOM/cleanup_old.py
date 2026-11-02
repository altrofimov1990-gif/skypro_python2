# cleanup_old.py
import requests

token = ""
with open(".env", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TOKEN_GLOBAL="):
            token = line.strip().split("=", 1)[1].strip()

headers = {
    "Cookie": f"token_global={token}",
    "Origin": "https://teachers.skyeng.ru",
    "Referer": "https://teachers.skyeng.ru/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/json",
}

r = requests.post(
    "https://api-teachers.skyeng.ru/v2/schedule/events",
    json={"from": "2026-11-01T00:00:00+03:00", "till": "2026-11-09T23:59:59+03:00", "onlyTypes": []},
    headers=headers,
)
events = r.json()["data"]["events"]
for ev in events:
    if ev.get("type") == "personal" and "Autotest" in ((ev.get("payload") or {}).get("title") or ""):
        ev_id = ev["payload"]["id"]
        resp = requests.post(
            "https://api-teachers.skyeng.ru/v2/schedule/removePersonal",
            json={"id": ev_id, "startAt": ev["startAt"]},
            headers=headers,
        )
        print(ev_id, ev["payload"].get("title"), "->", resp.json().get("errors") is None)
