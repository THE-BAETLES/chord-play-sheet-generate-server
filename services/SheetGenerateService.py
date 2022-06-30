import math
import pandas as pd
from music21 import converter, corpus, instrument, midi, note, chord, pitch, environment
class SheetGenerateService:
   
    def __init__(self, csv_path: str, midi_path: str) -> None:
        self.csv_path = csv_path
        self.midi_path = midi_path
    
    def open_midi(self, midi_path, remove_drums):
    # There is an one-line method to read MIDIs
    # but to remove the drums we need to manipulate some
    # low level MIDI events.
        mf = midi.MidiFile()
        mf.open(midi_path)
        mf.read()
        mf.close()
        if (remove_drums):
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]          

        return converter.parse(midi_path), mf

    def offset_to_sec(self, offset, bpm):
        return offset * (60 / bpm)


    def get_one_duration(self, bpm):
        """
            4분의 4박자가 전부 진행되는데 소요되는 시간을 구함
            params:
            bpm: wav file bpm information
            
        """
        return 4 * (60 / bpm)


    def get_bpm(self, midi_path):
        base_midi, midi = self.open_midi(midi_path, False)
        chordify_midi = base_midi.chordify()

        print(chordify_midi)

        bpm = chordify_midi[1].number

        print("bpm = ", chordify_midi[1])

        return bpm


    def get_position(self,start_time, one_durtaion):
        """
            params:
            one_duration: 4 * (60 / bpm)
        """

        return math.ceil(((start_time / one_durtaion -0.001) * 100) / 25)


    def make_sheet(self, bpm):
        csv = pd.read_csv(self.csv_path)
  
        dict_csv_iter = csv.itertuples()

        print("one_duration = ", self.get_one_duration(bpm))

        sheet = {
            'bpm': bpm,
            'info': [{
                'chord': info.chord,
                'start': info.start,
                'end': info.end,
                'position': self.get_position(info.start, self.get_one_duration(bpm))
                } for info in dict_csv_iter]
        }

        # print("sheet: ", sheet)
        return sheet

    def start(self):
        bpm = self.get_bpm(self.midi_path)
        sheet = self.make_sheet(bpm)

        return sheet