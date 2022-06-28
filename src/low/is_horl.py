import matplotlib.pyplot as plt
import pandas as pd
from hangul_utils import split_syllables, join_jamos
import re
#from eunjeon import Mecab
from konlpy.tag import Mecab
import low_utils as util
import dictionary as dic


mec = Mecab()


class isHigh(object):

    def __init__(self):
        
        mec = Mecab()

    def is_high(self, input, lis_ef, tag_last, lis_w_last, lis_w_last_not):
    
        lis_res_word = []
    
        lis_input = input.split()
        lis_word = []
        lis_tag = []
        lis_last_word = []
        lis_ind = []
        lis_ind_ele = []
    
        lis_result = []
    
        for i in range(len(lis_input)):
            ele_w = []
            ele_t = []
        
            an = mec.pos(lis_input[i])
            for j in range(len(an)):
                ele_w.append(an[j][0])
                ele_t.append(an[j][1])
            elem_w = ' '.join(ele_w)
            elem_t = '/'.join(ele_t)
        
            jam_pre = util.Jamodealer(elem_w)
            lis_word.append(''.join(jam_pre.jamo))
            lis_tag.append(elem_t)
    
        for i in range(len(lis_tag)):
        
            if 'EF/SF' in lis_tag[i] or 'EF/SV' in lis_tag[i] or 'EC/SY'  in lis_tag[i] or 'EC/SF' in lis_tag[i] or 'EC/SSO' in lis_tag[i] or 'IC/SF' in lis_tag[i]:
                elemen_t = lis_tag[i].split('/')
                elemen_w = lis_word[i].split(' ')
                flag = 0
                ff=0
            
#             print('iiii')
            
                for j in range(len(elemen_t)):

                    flag_end = jam_pre.detect_h(elemen_w[j], lis_w_last_not, lis_w_last)
                
                    if flag_end==1:
                    
                        return 1
                    else:
                    
                        return 0
    def isThisHigh(self, input):

        return self.is_high(input, dic.lis_beta_ef, dic.lis_tag_last, dic.lis_end_2low, dic.lis_end)
    
    def getState(self, detect):
        if detect == 0:
            print("다음 문장은 반말입니다. 문장이 변경되지 않습니다.")
        elif detect ==1:
            print("다음 문장은 높임말입니다. 문장을 반말로 변경합니다.")
        else:
            print("제대로 판별하지 못했습니다.")
            