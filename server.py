from dotenv import load_dotenv
from services.EssensiaSheetGenerateService import EssentiaSheetGenerateService
from fastapi import FastAPI, Query
from typing import List
load_dotenv()
app = FastAPI()


def test_deco(flask_func):
    print("Hello")
    def inner(*args, **kwargs):
        print("Hello Deco")
        print(args, kwargs)
        return flask_func(*args, **kwargs)
    return inner
        
@app.get('/sheet')
async def sheet(csv_path: str, midi_path: str, bpm: float, beats: List[float]) -> str:
    
    with EssentiaSheetGenerateService(bpm, beats, csv_path, midi_path) as sheetService:
        sheet = sheetService.start()
    return sheet


@test_deco
@app.get('/test')
async def test(arr: str):
    arr_list = list(map(lambda x: float(x), arr[1:-1].split(',')))
    print(arr_list)
    print(type(arr_list))
    return arr

@app.get('/healthCheck')
async def healthCheck(test:str):
    
    
    return "I`m Healthy now"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1203)
