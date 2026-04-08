from fastapi import FastAPI, Request
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
import random
from urllib.parse import quote

app = FastAPI()

app.mount("/music", StaticFiles(directory="/root/alice/music/"), name='music')

Base_url = "https://127.0.0.1:5000/music"

playlist = [
    {"id": "track_1", "title": "Разбуди", "file": "01_Разбуди.mp3"},
    {"id": "track_2", "title": "Мама просила", "file": "02_Мама_просила.mp3"},
    {"id": "track_3", "title": "Мать земля", "file": "03_Мать_земля.mp3"},
    {"id": "track_4", "title": "Темная сторона", "file": "04_Темная_сторона-SOROKAA.mp3"},
    {"id": "track_5", "title": "Лес", "file": "05_Лес.mp3"},
    {"id": "track_6", "title": "Манифест", "file": "06_Манифест-SOROKAA.mp3"},
    {"id": "track_7", "title": "Тело", "file": "07_Тело.mp3"},
    {"id": "track_8", "title": "Мне так", "file": "08_Мне_так.mp3"},
    {"id": "track_9", "title": "Научи любить", "file": "09_Научи_любить.mp3"},
    {"id": "track_10", "title": "Церемония", "file": "10_Церемония.mp3"},
    {"id": "track_11", "title": "Умри печаль", "file": "11_Умри_печаль-SOROKAA.mp3"}
]

@app.post("/")
async def alice(request: Request):
    data = await request.json() 
    version = data.get("version")
    session = data.get("session")
    request_obj = data.get("request", {})
    meta = data.get("meta", {})

    req_type = request_obj.get("type")
    print(f"Тип запроса: {req_type}")

    original = request_obj.get("original_utterance", "").lower()
    intents = request_obj.get("nlu", {}).get("intents", {})

    interfaces = meta.get("interfaces", {})
    has_player = "audio_player" in interfaces
    welcome_text = "Привет! Это официальный навык группы Сорока. Я могу включить наши песни. Просто скажите: включи музыку."
    welcome_tts = "Прив+ет! Эио офици+альный н+авык гр+уппы Сор+ока. Я мог+у включ+ить н+аши п+есни. Пр+осто скаж+ите: включ+и м+узыку."
    track = random.choice(playlist)
    encoded_file = quote(track['file'])
    track_url = f"{Base_url}/{encoded_file}"

    if req_type and "AudioPlayer" in req_type:
        if req_type == "AudioPlayer.PlaybackStarted":
            print("Трек начал играть")
        return {
            "version": version,
            "session": session,
            "response": {"end_session": False}
        }


    if session.get("new"):
        return {
            "version": version,
            "session": session,
            "response": {
                "text": welcome_text,
                "tts": welcome_tts,
                "end_session": False
            }
        }
    if "YANDEX.HELP" in intents or "помощь" in original or "что ты умеешь" in original:
        return {
            "version": version,
            "session": session,
            "response": {
                "text": "Я умею находить и включать песни группы Сорока. Чтобы начать слушать, скажите 'Включи музыку'. Что выберете?",
                "tts": "Я ум+ею наход+ить и включ+ать п+есни гр+уппы Сор+ока. Чт+обы нач+ать сл+ушать, ск+ажите: включ+и м+узыку. Что выберете?",
                "end_session": False
            }
        }

    if not original or any(word in original for word in ["включи", "музык", "песн", "давай"]):
        track = random.choice(playlist)
        encoded_file = quote(track['file'])
        track_url = f"{Base_url.rstrip('/')}/{encoded_file}"
        
        print(f"Отправляю в Алису: {track_url}")
        
        return {
            "version": version,
            "session": session,
            "response": {
                "text": f"Включаю {track['title']} группы Сорока",
                "directives": {
                    "audio_player": {
                        "action": "Play",
                        "item": {
                            "stream": {
                                "url": track_url,
                                "offset_ms": 0,
                                "token": track['id']
                            },
                            "metadata": {
                                "title": track['title'],
                                "sub_title": "Группа Сорока"
                            }
                        }
                    }
                },
                "end_session": False
            }
        }
    if request_obj.get("type") == "AudioPlayer.PlaybackStarted":
        return {"version": version, "session": session, "response": {"end_session": False}}
    return {
        "version": version,
        "session": session,
        "response": {
            "text": "Привет! Я могу включить музыку группы Сорока. Просто скажите: включи музыку.",
            "tts": "Прив+ет! Я мог+у включ+ить м+узыку гр+уппы Сор+ока. Пр+осто скаж+ите: включ+и м+узыку.",
            "end_session": False
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)