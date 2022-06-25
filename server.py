from flask import app, Flask, request,  jsonify
from dotenv import load_dotenv
from services.SheetGenerateService import SheetGenerateService
import os
load_dotenv()
app = Flask(__name__)


@app.route('/sheet', methods=["POST"])
def sheet() -> str:
    request_params = request.args.to_dict()
    
    csv_path: str = request_params["csvPath"]
    midi_path: str = request_params["midiPath"]
    
    service = SheetGenerateService()
    sheet = service.start()


    return jsonify(sheet)

if __name__ == '__main__':

    pass

