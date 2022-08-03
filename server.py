from flask import app, Flask, request,  jsonify
from dotenv import load_dotenv
from services.SheetGenerateService import SheetGenerateService
import os
load_dotenv()
app = Flask(__name__)

listen_port = os.environ.get("SERVER_PORT")
@app.route('/sheet', methods=["GET"])
def sheet() -> str:
    request_params = request.args.to_dict()
    
    print(request_params)
    csv_path: str = request_params["csvPath"]
    midi_path: str = request_params["midiPath"]
    
    with SheetGenerateService(csv_path, midi_path) as sheetService:
        sheet = sheetService.start()
        
    return jsonify(sheet)

if __name__ == '__main__':
    print(f"[Sheet Generate Engine Server] start listen on {1203}")
    app.run(host='0.0.0.0', port=1203)
