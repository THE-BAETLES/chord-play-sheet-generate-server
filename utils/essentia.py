from typing import Tuple, List
from time import time

def pull_position_info(beat_infos, align_pos_info):
    """
    window_sliding
     sliding_length: 4
    """
    from collections import deque
    
    start_pos_index = -1
    for i in range(len(align_pos_info) - 4):
        
        chk_cnt = 0
        
        for j in range(1, 4):
            if align_pos_info[i+j] - align_pos_info[i+j-1] <= 4:
                chk_cnt += 1
                
        if chk_cnt == 3:
            start_pos_index = i
            break
    
    print("start position = ",start_pos_index)
    
    start_pos = align_pos_info[start_pos_index]
    
    if start_pos % 4 == 0:
        return beat_infos, align_pos_info
    
    psum = beat_infos[start_pos - 1]
    
    fix_beat = psum / 4
    
    new_beat = deque(beat_infos[start_pos:])
    
    sum = 0
    
    
    for i in range(1, 5):
        print(fix_beat * i)
        new_beat.appendleft(fix_beat * (5-i))
        
    for i in range(len(align_pos_info)):
        if align_pos_info[i] >= start_pos:
            align_pos_info[i] -= (start_pos - 4)
            
    return new_beat, align_pos_info
        
def get_align_position_info(beat_infos, sheet):
    """
        sheet:
            position, spos, epos
            
    case1: 이전 pos 와 4 초과 차이가 존재 할 경우
            그 차이가 5일 경우
            - 현재 start 값이 beat_info[s_pos - 1] 와 0.3초 이하로 차이날 경우
            - 현재 pos - 1 함
            
            차이가 6이상일 경우
            
            - 그냥 넘겨버림
    case2: 이전 pos 와 4 이하가 차이날 경우
            - 현재 s_pos 와 e_pos 사이에 이전 pos 와 4이상 차이나는 구간이 존재할경우 해당 Pos로 바꿈
            - 사이에 4 차이나는 구간이 없고 3 이하가 차이날 경우
                - Position 은 2 만큼 차이나는 것으로 가정
    
    """
    
    pos_info = [info['spos'] for info in sheet['info']]
    chord_info = [info['chord'] for info in sheet['info']]
    
    for i, info in enumerate(sheet['info']):
        if i == 0:
            continue
            
        before_pos = pos_info[i-1]
        
        cur_start, cur_end = info['start'], info['end']
        cur_s_pos, cur_e_pos = info['spos'], info['epos']
        
        pos_distance = cur_s_pos - before_pos
        
        if pos_distance > 4:
            if pos_distance == 5 and cur_start - beat_infos[cur_s_pos - 1] < 0.3:
                pos_info[i] = cur_s_pos - 1
        
        
        if pos_distance < 4:
            if cur_e_pos >= before_pos + 4:
                pos_info[i] = before_pos + 4
                
            else:
                # 3이하 차이가 날 경우
                pos_info[i] = before_pos + 2
            continue
    
    for i, info in enumerate(pos_info):
        if pos_info[i] % 2 != 0:
            pos_info[i] -= 1
            
        
    return pos_info, chord_info
        