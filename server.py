from dotenv import load_dotenv
from services.EssensiaSheetGenerateService import EssentiaSheetGenerateService
from fastapi import FastAPI
from typing import List
load_dotenv()
app = FastAPI()

@app.get('/sheet')
async def sheet(csv_path: str, midi_path: str, bpm: float, beats: List[float]) -> str:
    with EssentiaSheetGenerateService(bpm, beats, csv_path, midi_path) as sheetService:
        sheet = sheetService.start()
    return sheet

@app.get('/healthCheck')
async def healthCheck():
    return "I`m Healthy now"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1203)
