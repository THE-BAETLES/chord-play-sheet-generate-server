from typing import Tuple, List
import essentia.standard as es
from time import time

def get_bpm_beat_info(audio_path: str) -> Tuple[int, List]:
    detection_start_time = time()
    print("Beat detection start!!")
    
    audio = es.MonoLoader(filename=audio_path)()
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
    
    print(f"Beat detection end on {time() - detection_start_time}s")
    
    return bpm, beats