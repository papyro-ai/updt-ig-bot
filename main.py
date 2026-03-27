from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
import pandas as pd
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_URL = os.getenv("SHEET_URL")


def send_post(image_url, caption):
    url_photo = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    url_message = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # baixa imagem
    img = requests.get(image_url).content

    # se legenda for pequena → envia normal
    if len(caption) <= 1024:
        response = requests.post(
            url_photo,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={
                "photo": ("image.jpg", img)
            }
        )

        print("STATUS:", response.status_code)
        print("RESPOSTA:", response.text)

    else:
        # corta legenda
        first_part = caption[:1024]
        rest = caption[1024:]

        # envia imagem com primeira parte
        response1 = requests.post(
            url_photo,
            data={
                "chat_id": CHAT_ID,
                "caption": first_part
            },
            files={
                "photo": ("image.jpg", img)
            }
        )

        print("STATUS FOTO:", response1.status_code)
        print("RESPOSTA FOTO:", response1.text)

        # envia restante como texto
        response2 = requests.post(
            url_message,
            data={
                "chat_id": CHAT_ID,
                "text": rest
            }
        )

        print("STATUS TEXTO:", response2.status_code)
        print("RESPOSTA TEXTO:", response2.text)


def main():
    df = pd.read_csv(SHEET_URL)

    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    window_start = now - timedelta(minutes=4)

    print("CHAT_ID:", CHAT_ID)
    print("TOKEN:", TOKEN)
    print("Agora:", now)

    for _, row in df.iterrows():
        post_time = datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M")
        post_time = post_time.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

        print("Post:", post_time)

        if window_start <= post_time <= now:
            send_post(row["image_url"], row["caption"])
            print("Enviado:", row["caption"])


if __name__ == "__main__":
    main()