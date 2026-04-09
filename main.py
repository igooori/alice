from fastapi import FastAPI, Request
import uvicorn
from fastapi.staticfiles import StaticFiles
import os
import random
from urllib.parse import quote
import urllib.parse

app = FastAPI()

app.mount("/music", StaticFiles(directory="/var/www/music/"), name='music')

Base_url = "https://sorokaa-bot.ru/music"

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
    session = data.get("session", {})
    request_obj = data.get("request", {})
    meta = data.get("meta", {})

    req_type = request_obj.get("type")
    
    if req_type and "AudioPlayer" in req_type:
        return {
            "version": version,
            "session": session,
            "response": {"end_session": False}
        }

    original = request_obj.get("original_utterance", "").lower()
    intents = request_obj.get("nlu", {}).get("intents", {})

    if session.get("new"):
        return {
            "version": version,
            "session": session,
            "response": {
                "text": "Привет! Это официальный навык группы Сорока. Я могу включить наши песни. Просто скажите: включи музыку.",
                "tts": "Прив+ет! Это офици+альный н+авык гр+уппы Сор+ока. Я мог+у включ+ить н+аши п+есни. Пр+осто скаж+ите: включ+и м+узыку.",
                "end_session": False
            }
        }

    if not original or any(word in original for word in ["включи", "музык", "песн", "давай"]):
        track = random.choice(playlist)
        file_name = track['file']
        encoded_file = quote(file_name)
        
        track_url = f"https://sorokaa-bot.ru/music/{encoded_file}"
        # track_url = "https://yandex.net"
        
        print(f"DEBUG: Отправляю URL -> {track_url}")
        
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
                                "token": str(track['id']) # Токен строго строкой
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
    return {
        "version": version,
        "session": session,
        "response": {
            "text": "Я могу включить музыку группы Сорока. Скажите 'включи музыку'.",
            "end_session": False
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)