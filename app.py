from flask import Flask, request
import requests

app = Flask(__name__)

PUSHOVER_TOKEN = "acbc3qetkd341664db3xgh3bts4ysz"
PUSHOVER_USER = "uhe71aw8vzffvg38y8xk7vsnnafeq4"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1361851340933959902/8nESdINoJzK72m7I9c8Kp8mr80IfuHiK3t1rICyjP3S8NQ1DPkEegjhXwhz4l0_wDPny"

@app.route('/', methods=['POST'])
def handle_webhook():
    data = request.json

    message = "🎫 Places disponibles !\n"
    if 'message' in data:
        message += data['message']
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