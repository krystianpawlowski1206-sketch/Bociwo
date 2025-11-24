from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ BOT DZIAŁA KURWA 123"

def run():
    app.run(host="0.0.0.0", port=5000)

def keep_alive():
    server = Thread(target=run)
    server.start()