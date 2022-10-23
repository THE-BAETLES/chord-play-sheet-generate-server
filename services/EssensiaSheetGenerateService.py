
import numbers
from services.BaseSheetGenerateService import BaseSheetGenerateService
from services.ResponseDataGenerateService import ResponseDataGenerateService

from utils.essentia import get_align_position_info,get_bpm_beat_info, pull_position_info
from utils.essentia import get_bpm_beat_info
from typing import List
import pandas as pd

class EssentiaSheetGenerateService(BaseSheetGenerateService):
    def __init__(self, csv_path, midi_path, bpm, beats) -> None:
        super(self)
        self.csv_path = csv_path
        self.midi_path = midi_path
        self.bpm = bpm
        self.beats = beats
        
    def get_position(self, beat_info_list, value):
        
        """
            beat_info_list: list of beat info which indicate onset beat second
        """
        def find_pos_bs(value):
            s_index = 0
            e_index = len(beat_info_list) - 1
            
            while s_index < e_index:
                m_index = (s_index + e_index) // 2
                beat_onset = beat_info_list[m_index]
                
                # 만약 값이 value 보다 크면
                if beat_onset > value:
                    e_index = m_index
                else:
                    s_index = m_index + 1
                    
            return s_index
        
        pos = find_pos_bs(value)
        
        return pos
    def compress_sheet_info(self, sheet_info):
        """
            sheet_info: pandas_object
            같은 코드가 여러번 반복될 경우 합침
            
        """
        compress_sheet_info = []
        before_chord = ":"
        before_end = -1
        before_start = -1
        
        compress_threshold = 2
        
        for info in sheet_info:
            # 이전 코드가 현재 코드와 같을 경우
            if before_chord == info['chord']:
                if before_end - before_start >= compress_threshold:
                    compress_sheet_info.append(
                        {
                            'chord': before_chord,
                            'start': before_start,
                            'end': before_end
                        }
                    )
                    before_start = info['start']
                before_end = info['end']
            # 다를 경우
            else:

                # 만약 시작 코드가 아닐 경우
                if before_chord != ":":
                    compress_sheet_info.append(
                        {
                            'chord': before_chord,
                            'start': before_start,
                            'end': before_end
                        }
                    )
                    
                # 현재 시작점 설정
                before_start = info['start']
                before_chord = info['chord']
                before_end = info['end']
        
        return compress_sheet_info
    
    def filter_sheet_info(self, sheet_info):
        """
            inference 결과가 0.5 미만일 경우 제외함
        """
        return list(filter(lambda x: (x['end'] - x['start']) >= 0.8 , sheet_info))
    
    
    def make_sheet(self):
        csv = pd.read_csv(self.csv_path)
        dict_csv_iter = csv.itertuples()
        
        dict_csv_iter = [
            {'chord': info.chord,
             'start' : info.start,
             'end': info.end
            } for info in dict_csv_iter
        ]
        
        dict_csv_iter = self.compress_sheet_info(dict_csv_iter)
        dict_csv_iter = self.filter_sheet_info(dict_csv_iter)
        dict_csv_iter = self.compress_sheet_info(dict_csv_iter)
        
        sheet = {
            'bpm': self.bpm,
            'info': [{
                'chord': info['chord'],
                'start': info['start'],
                'end': info['end'],
                'spos': self.get_position(self.beats, info['start']),
                'epos': self.get_position(self.beats, info['end'])
                } for info in dict_csv_iter]
        }
        
        pos_info, chord_info = get_align_position_info(self.beats, sheet)
        new_beat, align_pos_info = pull_position_info(self.beats, pos_info)
        
        response_service = ResponseDataGenerateService(self.bpm, new_beat, align_pos_info, chord_info)
        response_sheet = response_service.get_res_sheet_data()
        
        return response_sheet
    
    
    def start(self):
        return self.make_sheet()
                