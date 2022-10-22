from dotenv import load_dotenv
from services.SheetGenerateService import SheetGenerateService
from fastapi import FastAPI

load_dotenv()
app = FastAPI()

@app.get('/sheet')
async def sheet(csv_path: str, midi_path: str) -> str:
    with SheetGenerateService(csv_path, midi_path) as sheetService:
        sheet = sheetService.start()
    return sheet

@app.get('/healthCheck')
async def test():
    return "I`m Healthy now"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1203)
