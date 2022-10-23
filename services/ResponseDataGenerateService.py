from asyncio.windows_events import NULL
from macpath import split


class ResponseDataGenerateService:
    def __init__(self,bpm, beat_info, pos_info, sheet):
        self.beat_info = beat_info
        self.pos_info = pos_info
        self.sheet = sheet
        self.bpm = bpm
    
    def split_chord(self,chord):
        """_summary_

        Args:
            chord: A:min
        """
        root, triad = chord.split(':')
        return root, triad, 'none'
    
    def get_res_sheet_data(self):
        
        chord_infos = []
        
        for i, info in enumerate(self.sheet['info']):
            
            root, triad, bass = self.split_chord(info['chord'])
            
            chord_infos.append({
                'start': info['start'],
                'end': info['end'],
                'root': root,
                'triad': triad,
                'bass': bass,
                'position': self.pos_info[i]
            })
        
        return {
            'bpm': self.bpm,
            'beatInfos:' : self.beat_info,
            "chordInfos": chord_infos
        }