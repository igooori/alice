from fastapi import FastAPI, Request
import uvicorn
import random
from fastapi.responses import HTMLResponse 

app = FastAPI()

playlist = [
    {
        "id": "track_1", 
        "title": "Разбуди", 
        "audio_ids": [
            "22b0f727-6feb-48bf-88d4-a021b50094a9", 
            "6254af1e-a0b1-4717-ba9d-4c10677a8e91"
        ]
    },
    # Сюда добавишь остальные треки по аналогии, когда загрузишь их в Ресурсы
]

SKILL_ID = "a0dabc80-276f-40db-bcab-fe7e9c9c0e80"

@app.get("/yandex_abed135471139a33.html")
async def verify():
    content = "<html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8'></head><body>Verification: abed135471139a33</body></html>"
    return HTMLResponse(content=content)

@app.post("/")
async def alice(request: Request):
    data = await request.json() 
    version = data.get("version")
    session = data.get("session", {})
    request_obj = data.get("request", {})

    original = request_obj.get("original_utterance", "").lower()

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
        
        tts_parts = ""
        for audio_id in track["audio_ids"]:
            tts_parts += f"<speaker audio='dialogs-upload/{SKILL_ID}/{audio_id}.opus'>"
        
        print(f"DEBUG: Играю трек {track['title']}")

        return {
            "version": version,
            "session": session,
            "response": {
                "text": f"Включаю песню {track['title']} группы Сорока.",
                "tts": f"Включ+аю п+есню {track['title']} гр+уппы Сор+ока. {tts_parts}",
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