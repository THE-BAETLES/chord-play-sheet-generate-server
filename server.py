from dotenv import load_dotenv
from services.EssensiaSheetGenerateService import EssentiaSheetGenerateService
from fastapi import FastAPI, Query
from utils.request import string_to_float_list
from typing import List
from models.SheetRequest import SheetRequestModel

load_dotenv()
app = FastAPI()

@app.post('/sheet')
async def sheet(sheetRequest: SheetRequestModel):
    with EssentiaSheetGenerateService(sheetRequest.csv_path, sheetRequest.midi_path,sheetRequest.bpm, sheetRequest.beats) as sheetService:
        sheet = sheetService.start()
    return sheet

@app.get('/healthCheck')
async def healthCheck(test:str):
    return "I`m Healthy now"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1203)
