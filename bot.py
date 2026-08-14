from flask import Flask, request
import requests
import os
import re
import random

app = Flask(__name__)

# -----------------------------
# CONFIG
# -----------------------------

BOT_ID = os.environ.get("BOT_ID")

# -----------------------------
# NIKO BANNED WORDS
# -----------------------------

NIKO_ONLY_BANNED_WORDS = [
    "eva",
    "rene",
    "brendon",
    "drill sergeant",
    "clanker",
    "shh",
    "hehe",
    "haha",
    "die",
    "kill",
    "stupid",
    "dumb",
    "mom",
    "dad",
    "shhh",
    "idiot",
    "ass",
    "shut",
    "uncle",
    "aunty",
    "what",
    "no",
    "stop",
    "fine"
]

# -----------------------------
# STORAGE
# -----------------------------

niko_message_count = 0

# -----------------------------
# SEND MESSAGE
# -----------------------------

def send_message(text):

    if not BOT_ID:
        print("BOT_ID missing")
        return

    try:
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": BOT_ID,
                "text": text
            },
            timeout=10
        )

    except Exception as error:
        print(
            "Error sending GroupMe message:",
            error
        )

# -----------------------------
# WEBHOOK
# -----------------------------

@app.route("/", methods=["POST"])
def webhook():

    global niko_message_count

    data = request.json

    if not data:
        return "ok", 200

    # Ignore bot messages
    if data.get("sender_type") == "bot":
        return "ok", 200

    name = data.get(
        "name",
        "Unknown"
    )

    name_lower = name.lower()

    message = data.get(
        "text",
        ""
    ).strip()

    message_lower = message.lower()

    # -----------------------------
    # ONLY WATCH NIKO
    # -----------------------------

    if "niko" not in name_lower:
        return "ok", 200

    # -----------------------------
    # COUNT NIKO'S MESSAGES
    # -----------------------------

    niko_message_count += 1

    # -----------------------------
    # BANNED WORD CHECK
    # -----------------------------

    for word in NIKO_ONLY_BANNED_WORDS:

        if re.search(
            rf"\b{re.escape(word)}\b",
            message_lower
        ):

            send_message(
                f"{name}, please watch your language."
            )

            break

    # -----------------------------
    # EVERY 2ND MESSAGE
    # -----------------------------

    if niko_message_count % 2 == 0:

        stop_messages = [
            "Niko, please stop sending so many messages.",
            "Niko, please slow down with the messages.",
            "Niko, you've been talking a lot. Please stop for a moment.",
            "Niko, please give the chat a break.",
            "Niko, that's enough messages for now. Please stop.",
            "Niko, please stop flooding the chat.",
            "Niko, you've sent enough messages. Please stop.",
            "Niko, please chill with the messages.",
            "Niko, take a break from messaging for a bit.",
            "Niko, please stop messaging so much."
        ]

        send_message(
            random.choice(stop_messages)
        )

    return "ok", 200


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
