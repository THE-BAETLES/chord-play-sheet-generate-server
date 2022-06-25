class SheetGenerateService:
    def __init__(self, csv_path: str, midi_path: str) -> None:
        
        self.csv_path = csv_path
        self.midi_path = midi_path

        pass

    def get_bpm(self):
        pass

    def make_sheet(self, bpm):
        pass

    def start(self):
        bpm = self.get_bpm()
        sheet = self.make_sheet(bpm)
        
        return sheet