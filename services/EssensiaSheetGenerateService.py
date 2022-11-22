from services.BaseSheetGenerateService import BaseSheetGenerateService
from services.ResponseDataGenerateService import ResponseDataGenerateService
from utils.essentia import get_align_position_info, pull_position_info
from typing import List
import pandas as pd

class EssentiaSheetGenerateService(BaseSheetGenerateService):
    def __init__(self, csv_path, midi_path, bpm, beats) -> None:
        super()
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
        beat_onset = beat_info_list[pos]

        if pos != 0:
          left_beat_onset = beat_info_list[pos - 1]
          
          if abs(value - left_beat_onset) < abs(beat_onset - value):
            pos -= 1
        
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

    

    def split_chord(self,chord):
        """_summary_
        Args:
            chord: A:min
        """
        root, triad = chord.split(':')
        return root, triad, 'none'
    
    
    def make_sheet(self):
        csv = pd.read_csv(self.csv_path)
        dict_csv_iter = csv.itertuples()
        
        dict_csv_iter = [
            {
            'chord': info.chord,
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
        

        responseInfo = []

        # epos를 idx+1의 spos로 고정
        for idx, info in enumerate(sheet['info']):
          if idx < len(sheet['info']) - 1:
            info['epos'] = sheet['info'][idx + 1]['spos']


        # 앞에 비트 넣기 (align)
        appearCount = [0, 0, 0, 0]

        for idx, info in enumerate(sheet['info']):
          appearCount[info['spos'] % 4] += 1

        prefixCount = (4 - appearCount.index(max(appearCount)))

        alignedSheet = {
            'bpm': sheet['bpm'],
            'info': [],
        }
        
        newBeats = []
        
        for i in range(0, prefixCount):
          alignedSheet['info'].append({
              'chord': "none:none",
              'spos' : i,
              'epos' : i + 1,
          })

          newBeats.append(0)

        for i in range(prefixCount, prefixCount + sheet['info'][0]['spos'] % 4):
          alignedSheet['info'].append({
              'chord': "none:none",
              'spos' : i,
              'epos' : i + 1,
          })

        
        for idx, info in enumerate(sheet['info']):
          alignedSheet['info'].append({
              'chord': info['chord'],
              'spos': info['spos'] + prefixCount,
              'epos': info['epos'] + prefixCount
          })
        
        for i in range(0, len(beats)):
          newBeats.append(beats[i])

        sheet = alignedSheet

        # 보정
        for idx, info in enumerate(sheet['info']):
          if idx < prefixCount:
            continue;

          if info['spos'] % 4 == 1 and sheet['info'][idx - 1]['spos'] < info['spos'] - 1:
            # 두번째 칸 보정
            newInfo = {
                'chord': info['chord'],
                'spos': info['spos'] - 1,
                'epos': info['epos'],
            }
            
            sheet['info'][idx] = newInfo
            
            if idx > 0:
              preInfo = sheet['info'][idx - 1]

              newPreInfo = {
                'chord': preInfo['chord'],
                'spos': preInfo['spos'],
                'epos': preInfo['epos'] - 1,
              }
              
              sheet['info'][idx - 1] = newPreInfo

          
          elif info['spos'] % 4 == 3 and info['epos'] - info['spos'] >= 2:
            # 네번째 칸 보정
            newInfo = {
                'chord': info['chord'],
                'spos': info['spos'] + 1,
                'epos': info['epos'],
            }
            
            sheet['info'][idx] = newInfo
            
            if idx > 0:
              preInfo = sheet['info'][idx - 1]

              newPreInfo = {
                'chord': preInfo['chord'],
                'spos': preInfo['spos'],
                'epos': preInfo['epos'] + 1,
              }
              
              sheet['info'][idx - 1] = newPreInfo
            
            print(info)

        print(sheet)

        # 서식 맞춤
        newSheet = []

        for i in range(0, sheet['info'][0]['spos']):
          newSheet.append({
                'chord': {
                    'root': 'none',
                    'triad': 'none',
                    'bass': 'none' 
                },
                'beat_time': newBeats[i]
            })
        
        for idx, info in enumerate(sheet['info']):
          root, triad, bass = self.split_chord(info['chord'])
          
          newSheet.append({
              'chord': {
                  'root': root,
                  'triad' : triad,
                  'bass' : bass
              },
              'beat_time': newBeats[info['spos'] + 1]
          })

          for i in range(info['spos'] + 2, info['epos'] + 1):
            newSheet.append({
                'chord': {
                    'root': 'none',
                    'triad': 'none',
                    'bass': 'none' 
                },
                'beat_time': newBeats[i]
            })
            
        result = {
          'bpm': sheet['bpm'],
          'infos': newSheet
        }

        return result
    
    def start(self):
        return self.make_sheet()
