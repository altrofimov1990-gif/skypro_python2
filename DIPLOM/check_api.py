import requests

# Читаем токен из .env — никаких переменных в PowerShell
token = ""
with open(".env", encoding="utf-8") as f:
    for line in f:
        if line.strip().startswith("TOKEN_GLOBAL="):
            token = line.strip().split("=", 1)[1].strip()

assert token, "TOKEN_GLOBAL не найден в .env"

url = "https://api-teachers.skyeng.ru/v2/schedule/events"
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
payload = {
    "from": "2026-10-29T00:00:00+03:00",
    "till": "2026-10-29T23:59:59+03:00",
    "onlyTypes": [],
}
r = requests.post(url, json=payload, headers=headers)
print("Статус:", r.status_code)
print(r.text[:400])
