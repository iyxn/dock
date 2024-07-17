import asyncio
from fastapi import FastAPI, Request, HTTPException
from aiohttp import ClientSession
from aiocache import cached, SimpleMemoryCache
from dotenv import load_dotenv
import os

# load api key dari file env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# cek apakah api key sudah di set
if not API_KEY:
    raise ValueError("API_KEY belum di set di file .env!")
#objek untuk API dan cache
app = FastAPI()
cache = SimpleMemoryCache()

# ketika mengakses root/index utama
@app.get("/")
async def main():
    return {"message": "Selamat datang"}

# fungsi call api ke gemini
@cached(cache)
async def generate_text_async(prompt, api_params):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"
    # definisi header http request
    headers = {
        'Content-Type': 'application/json',
    }
    # definisi data json untuk mengirim prompt dari user dan konfigurasi parameter
    data = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': api_params
    }

    async with ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response: # mulai melakukan call API ke gemini (eksternal)
            if response.status != 200: # handling kesalahan
                raise HTTPException(status_code=response.status, detail=await response.text())
            return await response.json() # return respon dari API eksternal
    
#endpoint
@app.post("/generate")
async def generate_text_endpoint(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages") #parsing pesan / prompt
        params = body.get("generationConfig", {}) #parsing konfigurasi parameter gemini

        if not messages:
            raise HTTPException(status_code=400, detail="Pesan kosong !.") #jika pesan kosong

        response = await generate_text_async(messages, params) #call api ke fungsi generate_text_async
        return response

    except Exception as e: #handling kesalahan
        raise HTTPException(status_code=500, detail=str(e))
    

## REFERENSI
# https://snyk.io/advisor/python/aiocache/functions/aiocache.cached (cache)
# https://scrapeops.io/python-web-scraping-playbook/python-aiohttp-post-requests/ (aiohttp untuk http request)
# https://www.youtube.com/watch?v=iWS9ogMPOI0 (FastAPI)
# https://medium.com/@moraneus/mastering-pythons-asyncio-a-practical-guide-0a673265cf04 (pemrograman asinkronus)
