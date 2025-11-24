from keep_alive import keep_alive
from telethon import TelegramClient, events
import asyncio
import re
from typing import Optional

api_id = 22308891
api_hash = "00cc5f4ac21c96cd144c93572e18c8da"
client = TelegramClient("telethon_session", api_id, api_hash)

# ► LISTA GRUP ŹRÓDŁOWYCH
SOURCE_CHATS = [
    -1002021920659,
    -1001825774085,
    -1001727471568,
    -1001786854508,
    -1002511091091,
    -1001649018010,
    -1002924963255,
    -1001927131969,
    -1001627374464,
    -1002486349917,
    -1001785890425,
    -1002407687507,
    -1002051588739,
    -1001158207903,
    -1002383084444
]

TARGET_CHATS = [
    -1003277793700,
    -1003096887835,
    -7795495001
]

PREFIX = "⚠️UWAGA: WYKRYTO ŻYDA⚠️\n\n"

def is_menu_announcement(text: str) -> bool:
    if not text:
        return False
    txt = text.lower()
    block_words = [
        "menu","witam warszaw","kontakt ","kontakt","stacjonarnie","wysyłka",
        "inpost","Hacking","posiadam spore lc","wymagam weryfikacji"
    ]
    for w in block_words:
        if w in txt:
            return True
    price_patterns = [
        r"\b\d+\s*-\s*\d+\b",
        r"\b\d+\s*=\s*\d+\b",
        r"\b\d+\s*(pln|zł)\b"
    ]
    for p in price_patterns:
        if re.search(p, txt):
            return True
    lines = txt.splitlines()
    if sum(1 for l in lines if re.search(r"\d", l)) >= 4:
        return True
    return False

LOCATION_MAP = {
    "bemowo": "BEMOWO","wola": "WOLA","centrum": "CENTRUM","włochy": "WŁOCHY",
    "wlochy": "WŁOCHY","mokotów": "MOKOTÓW","mokotow": "MOKOTÓW","ursynów": "URSYNÓW",
    "ursynow": "URSYNÓW","praga": "PRAGA","tarchomin": "TARCHOMIN","gocław": "GOCŁAW",
    "goclaw": "GOCŁAW","ochota": "OCHOTA","bielany": "BIELANY","żoliborz": "ŻOLIBORZ",
    "zoliborz": "ŻOLIBORZ","powiśle": "POWIŚLE","powisle": "POWIŚLE","świętokrzyska": "ŚWIĘTOKRZYSKA",
    "swietokrzyska": "ŚWIĘTOKRZYSKA","górczewska": "WOLA","al. jerozolimskie": "CENTRUM",
    "marszałkowska": "CENTRUM","nowy swiat": "CENTRUM","nowy świat": "CENTRUM",
    "chmielna": "CENTRUM","saska kępa": "PRAGA POŁUDNIE","saska kepa": "PRAGA POŁUDNIE",
    "rondo daszyńskiego": "WOLA","rondo onz": "WOLA"
}

extra = {}
for k,v in list(LOCATION_MAP.items()):
    k_norm = k.lower().replace("ą","a").replace("ę","e").replace("ó","o").replace("ł","l").replace("ś","s").replace("ż","z").replace("ć","c").replace("ń","n")
    extra[k_norm] = v
LOCATION_MAP.update(extra)

def detect_location(text: str) -> Optional[str]:
    if not text:
        return None
    txt_norm = text.lower().replace("ą","a").replace("ę","e").replace("ó","o").replace("ł","l").replace("ś","s").replace("ż","z").replace("ć","c").replace("ń","n")
    for key in sorted(LOCATION_MAP.keys(), key=lambda x: -len(x)):
        if key in txt_norm:
            return LOCATION_MAP[key]
    return None

@client.on(events.NewMessage(chats=SOURCE_CHATS))
async def handler(event):
    raw_msg = event.message.message or ""
    sender = await event.get_sender()

    if is_menu_announcement(raw_msg):
        return

    msg = raw_msg.lower()

    trigger = ["kto ma","ktoś ma","ktos ma","kto posiada","kto ogarnia","ktoś ogarnia",
               "ktos ogarnia","szukam","kupie","kupię","wtb","need","poszukuje",
               "ogarnie ktoś","ogarnie ktos","ogarnia ktoś","ogarnia ktos","ktos","ktoś"]

    words = ["mef","m3f","m33f","mateusz","mati","xan","x@n","ox","oks","oksa","clon",
             "klon","kl0n","klony","buszek","ziolo","zioło","weed","w33d","buch",
             "eufo","speed","sp33d","4mmc","3mmc","4cmc","3cmc","coco","c0c0",
             "koka","k0ka","snow","śnieg","kamyk","mef","m3f","koka","koks","xtc",
             "md","trawa","zioło","grzyby"]

    if not any(t in msg for t in trigger): return
    if not any(w in msg for w in words): return

    try:
        username = getattr(sender,"username",None)
        if username:
            sender_info = f"@{username}"
        else:
            sender_info = sender.first_name if sender.first_name else f"id:{sender.id}"
    except:
        sender_info = "brak_nicku"

    detected_location = detect_location(raw_msg)

    header = PREFIX + f"📣 Od: {sender_info}\n\n"
    text_to_send = header + raw_msg
    if detected_location:
        text_to_send += f"\n\n📍 Lokalizacja: {detected_location}"

    media = getattr(event.message,"media",None)

    try:
        if media:
            for chat in TARGET_CHATS:
                await client.send_file(chat, media, caption=text_to_send)
            return
        for chat in TARGET_CHATS:
            await client.send_message(chat, text_to_send)
    except:
        for chat in TARGET_CHATS:
            await client.forward_messages(chat, event.message)

async def main():
    await client.start()
    print("BOT WYSTARTOWAŁ ✅")
    await client.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())