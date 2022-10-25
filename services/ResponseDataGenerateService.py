from asyncio.windows_events import NULL
from macpath import split
from typing import List

class ResponseDataGenerateService:
    def __init__(self,bpm, beat_info, pos_info:List[int], chord_info: List[str]):
        """_summary_

        Args:
            bpm (_type_): music average bpm info
            beat_info (_type_): music per bpm info
            pos_info (_type_): chord position info
            sheet (_type_): _description_
        """
        self.beat_info = beat_info
        self.pos_info: List[int] = pos_info
        self.chord_info: List[str] = chord_info
        self.bpm = bpm
        self._set_total_infos()
        
    def split_chord(self,chord):
        """_summary_

        Args:
            chord: A:min
        """
        root, triad = chord.split(':')
        return root, triad, 'none'
    
    def _set_total_infos(self):
        total_infos = []
        for i, beat_time in enumerate(self.beat_info):
            # 만약 해당 인덱스에 대한 정보가 존재 할 경우
            if i in self.pos_info:
                # assert chord_info and pos_info size exactly same
                pos_arr_index = self.pos_info.index(i)
                chord = self.chord_info[pos_arr_index]
                root, triad, bass = self.split_chord(chord)
                
                total_infos.append(
                    {
                        'root': root,
                        'triad': triad,
                        'bass': bass,
                        'beat_time': beat_time
                    }
                )
                continue
            
            total_infos.append(
                {
                    'root': "none",
                    'triad': "none",
                    'bass': "none",
                    'beat_time': beat_time
                }
            )
        
        self.total_infos = total_infos
            
    def get_res_infos(self):
        return self.total_infos
    