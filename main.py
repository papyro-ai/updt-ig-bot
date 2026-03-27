from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import pandas as pd
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_URL = os.getenv("SHEET_URL")

def send_post(image_url, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    
    img = requests.get(image_url).content
    
    requests.post(
        url,
        data={"chat_id": CHAT_ID, "caption": caption},
        files={"photo": img}
    )

def main():
    df = pd.read_csv(SHEET_URL)

    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    window_start = now - timedelta(minutes=3)

    for _, row in df.iterrows():
        post_time = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M")
        post_time = post_time.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
        print("Agora:", now)
        print("Post:", post_time)

        if window_start <= post_time <= now:
            send_post(row["image_url"], row["caption"])
            print("Enviado:", row["caption"])

if __name__ == "__main__":
    main()