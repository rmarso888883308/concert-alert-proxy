from flask import Flask, request
import requests

app = Flask(__name__)

PUSHOVER_TOKEN = "acbc3qetkd341664db3xgh3bts4ysz"
PUSHOVER_USER = "uhe71aw8vzffvg38y8xk7vsnnafeq4"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1361851344318632248/XQKadc8ykDsqKGjUVddnyu0Cds_4WIO0vc-PSm_9YS7Wv709exsD3Rk2o7PQfQO1iUHo"

@app.route('/', methods=['POST'])
def handle_webhook():
    data = request.json

    # Format joli du message
    message = "🎫 Places détectées !\n\n"
    if isinstance(data, dict):
        if 'event' in data: message += f"🎤 Événement : {data['event']}\n"
        if 'date' in data: message += f"📅 Date : {data['date']}\n"
        if 'price' in data: message += f"💶 Prix : {data['price']}\n"
        if 'places' in data: message += f"🎟️ Places : {data['places']}\n"

        # S'il y a des champs en plus
        for k, v in data.items():
            if k not in ['event', 'date', 'price', 'places']:
                message += f"🔸 {k} : {v}\n"
    else:
        message += str(data)

    # Envoi Discord
    requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

    # Envoi Pushover
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER,
        "message": message,
        "title": "🎟️ Concert trouvé !",
        "priority": 1
    })

    return {"status": "ok"}

if __name__ == '__main__':
    app.run()
