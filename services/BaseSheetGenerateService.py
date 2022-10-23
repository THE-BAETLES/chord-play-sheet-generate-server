import math
import pandas as pd
import os
from music21 import converter, corpus, instrument, midi, note, chord, pitch, environment


class BaseSheetGenerateService:
    def __init__(self) -> None:
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self):
        # Delete Resources
        # TODO: Update to Kubernetes Resource Delete
        pass
    
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
    
    
    def make_sheet(self):
        pass
    
    
    
    def start(self):
        pass