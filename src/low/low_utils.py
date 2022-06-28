"""
높임말 반말 변환 모듈 - utils
__author__ = 'Joowhan Kim (joowhan@handong.ac.kr)'
__copyright__ = ''
"""

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import pandas as pd
from hangul_utils import split_syllables, join_jamos
from tqdm.auto import tqdm
import re
import dictionary as dic
from khaiii import KhaiiiApi

############ For Window ############ 
#from eunjeon import Mecab
############ For Window ############ 

############ For Mac ############ 
from konlpy.tag import Mecab
############ For Mac ############ 


mec = Mecab()
khai = KhaiiiApi()

def detect_h(input, lis_end_h, lis_end_l):
    for i in lis_end_h:
        if len(input)>=len(i):
            if input[-len(i):]==i:
                return 1
            
    for i in lis_end_l:
        if len(input)>=len(i):
            if input[-len(i):]==i:
                return 0
            
    return -1

def unite(input, dict):
    for i in dict:
        input = re.sub(i[0],i[1],input)
    return input
    
## 자모 단위로 문장을 나누고 합칠 때 쓰는 class ##
class Jamodealer:
    jamo = []
    pp = ''
    #각 단어들을 받아와서 자모단위로 나눈다.
    def __init__(self,lis_word):
    
        self.jamo = []
        for i in lis_word:
            self.jamo.append(split_syllables(i))
            
    def detect_h(self, input, lis_end_h, lis_end_l):
        for i in lis_end_h:
            if len(input)>=len(i):
                if input[-len(i):]==i:
                    return 1
            
        for i in lis_end_l:
            if len(input)>=len(i):
                if input[-len(i):]==i:
                    return 0
            
        return -1

    def unite(self, input, dict):
        for i in dict:
            input = re.sub(i[0],i[1],input)
        return input
    
    ##사전에서 변환된 자모단위로 분리된 문장을 합칠 때 쓰는 함수이다.     
    def make_one(self):
        #list 형태로 저장된 자모들의 집합을 하나의 string pp에 저장한다. 
        self.pp = ''
        for i in self.jamo:
             self.pp= self.pp+i
        ##종성과 종성을 합쳐야 하는 경우가 있다면 합친다.        
        self.pp = unite(self.pp, dic.con_dict)
        
        #자모 단위의 string에서 자모 단위로 사전을 만들고 거기에 index를 부여한다.        
        chars = list(set(self.pp))
        char_to_ix = { ch:i for i,ch in enumerate(chars) }
        ix_to_char = { i:ch for i,ch in enumerate(chars) }
        
        #자모 단위로 분리되었던 문장을 다시 하나로 합친다.
        jamo_numbers = [char_to_ix[x] for x in self.pp]
        restored_jamo = ''.join([ix_to_char[x] for x in jamo_numbers])
        #합쳐진 문장을 return 한다.
        restored_text = join_jamos(restored_jamo)
        return restored_text

def to2lists(input):
    lis_word = []
    lis_tag = []
    #data = han.pos(input,ntags=22,flatten=True, join=False)
    data = mec.pos(input)
    for i in data:
        lis_word.append(i[0])
        lis_tag.append(i[1])
    return lis_word, lis_tag

def to2lists_khaiii(input):
    lis_word = []
    lis_tag = []
    analyzed = khai.analyze(input)  
    for data in analyzed:
        for morph in data.morphs:
            lis_word.append(morph.lex)
            lis_tag.append(morph.tag)
    return lis_word, lis_tag


def rememberSpace(lis, input):
    
    rlis = []
    
    for i in range(len(lis)):
        if lis[i]==input:
            rlis.append(i)
            
    for i in range(len(rlis)):
        rlis[i] = rlis[i]-i      
    return rlis

def convertSpace(lis_space,lis_lis):
    
    rlis = []
    k=0
    for i in range(len(lis_lis)):
        
        if k in lis_space:
            rlis.append(i)
            
        k = k+len(lis_lis[i])
        
    #print(rlis)  
    return rlis

def union(lis, lis_lis):
    
    k = 0
    for i in lis:
        lis_lis.insert(i+k,' ')
        k = k+1

def union_t_03(lis_tag):
    
    for i in range(1, len(lis_tag)):
        if lis_tag[i-1] ==' ' or lis_tag[i]==' ':
            lis_tag[i] = lis_tag[i]
        else:
            lis_tag[i] = '/'+lis_tag[i]
            
def union_w_03(lis_w, lis_tag):
    
    for i in range(1, len(lis_w)):
        if lis_tag[i]==' SF':
            lis_w[i] = ' '+lis_w[i+1]
def proc_khaiii_with_Tag(input):
    
    r_sen = input
    
    res1 = ''
    res2 =''
    slis = []
    for i in range(len(input)):
        if r_sen[i]==' ':
            slis.append(1)
        elif r_sen[i]=='  ':
            slis.append(2)
            
    wlis = r_sen.split(' ')
    
    uu = khai.analyze(wlis[0])
    
    elem = ''
    tag =''
    
    for data in uu[0].morphs:
        elem = elem + data.lex+'/'
        tag = tag+data.tag+'/'
    
    res1 = res1+elem
    res2 = res2+tag
    
    for i in range(len(slis)):
        elem = ''
        tag = ''
        elem = elem+slis[i]*' '
        if i != len(wlis)-1:
            uu = khai.analyze(wlis[i+1])
            for data in uu[0].morphs:
                elem = elem+data.lex+'/'
                tag = tag+data.tag+'/'
        res1 = res1+elem
        res2 = res2+tag
    return res1,res2


########################## preprocessing with Khaiii ##########################

def prepro_khaiii(input):
    lis_w, lis_t = to2lists_khaiii(input)

    space_list = rememberSpace(input,' ')
    space_location = convertSpace(space_list, lis_w)
    union(space_location, lis_w)
    union(space_location, lis_t)
    union_t_03(lis_t)
    union_w_03(lis_w, lis_t)
    
    str_w = ''
    str_t = ''
    for i in range(len(lis_w)):
        str_w = str_w + lis_w[i]
        str_t = str_t + lis_t[i]
    
    data_w = str_w.split(' ')
    data_t = str_t.split(' ')
    
    lis_word, lis_tag = to2lists_khaiii(input)
    
    lis_ind = []
    t_ind = 0
    jam1 = Jamodealer(lis_word)
    jam2 = Jamodealer(data_w)
    for i in range(len(data_w)):
        element = []
        leng = len(data_t[i].split('/'))
        res = jam2.jamo[i]
        ind = 0
        lenlen = 0
        #element.append(0)
        for j in range(leng):
            element.append(ind)
            ind = ind + len(jam1.jamo[t_ind])
            res = res[len(jam1.jamo[t_ind]):]
            
            lenlen = len(jam1.jamo[t_ind])+lenlen
            t_ind = t_ind+1

        element.append(len(jam2.jamo[i]))
        lis_ind.append(element)
        
    return data_w, data_t, lis_ind


def prepro_beta_khaiii(input, lis_ef, tag_last, lis_w_last, lis_w_last_not):
    data_w, data_t, lis_ind = prepro_khaiii(input)
    
    last_words = []

    data_w_jamo = []

    data_t_after = []
    
    lis_target_ind = []
    
    for i in data_w:
        jam_ele = Jamodealer(i)
        ele = ''
        for j in jam_ele.jamo:
            ele = ele+j
        data_w_jamo.append(ele)
    
    for i in range(len(data_t)):
        #if i<len(data_t)-1:
        if i<len(data_t):
            lis_res = []
            for ind in range(len(lis_ind[i])-1):
                lis_res.append(data_w_jamo[i][lis_ind[i][ind]:lis_ind[i][ind+1]])

        
        if 'EF/SF' in data_t[i] or 'EF/SV' in data_t[i] or 'UNKNOWN/SF' in data_t[i] or 'UNKNOWN/SV' in data_t[i]:# and 'EC/SF' not in data_t[i]:
            if 'EF/SF' in data_t[i] or 'UNKNOWN' in data_t[i]:
                elements = data_t[i].split('/')
                flag = 0

                for j in range(len(elements)):
                
                    flag_end = detect_h(lis_res[j], lis_w_last,  lis_w_last_not)

                    if elements[j] in lis_ef and flag_end==1: #and j == len(elements)-1:

                        elements[j] = 'NULL'
                    
                        last_words.append(data_w_jamo[i][lis_ind[i][j]:lis_ind[i][j+1]])
                        lis_res[j]=''
                    
                        lis_target_ind.append(i)
                    
                        
                    elif 'EF' in elements[j] and flag_end==1:# + EF를 처리하는 부분이므로 + EF 만을 마지막에서 처리한다.
                        for jam in lis_w_last:
                            if len(lis_res[j])>=len(jam):

                                res_out_punc = lis_res[:lis_ind[i][-2]][j]

                                if res_out_punc[-len(jam):]==jam:

                                    #print(jam)
                                    lis_target_ind.append(i)
                                
                                    last_words.append(jam)
                                    lis_res[j] = lis_res[j].replace(jam, '', 1)

                                    for k in tag_last:

                                        if k in elements[j]:
                                        
                                            if '+' in elements[j]:
                                            
                                                ind = elements[j].index('+'+k)
                                                elements[j] = elements[j][:ind]
                                    break
                                
                                elif lis_w_last.index(jam)==len(lis_w_last)-1:#new
                                    for k in tag_last:

                                        if k in elements[j]:
                                        
                                            if '+' in elements[j]:
                                            
                                                ind = elements[j].index('+'+k)
                                                elements[j] = elements[j][:ind]
                                            
                                    lis_target_ind.append(i)
                                    last_words.append('')
                                    break

                
                elements_post = '/'.join(elements)
                data_t_after.append(elements_post)
                
                data_w_jamo[i] = ''.join(lis_res)

            
        elif 'EC/SF' in data_t[i] or 'JX/SF' in data_t[i]:
            elements = data_t[i].split('/')
            
            flag = 0
            for j in range(len(elements)):
                
                flag_end = -1
                if 'EC' in elements[j] or 'JX' in elements[j]:
                    flag_end = detect_h(lis_res[j], lis_w_last, lis_w_last_not)

                if flag_end==1 and i not in lis_target_ind:
                    for jam in lis_w_last:

                        if len(jam)<=len(lis_res[j]):
                            #print(lis_res[j])
                            if lis_res[j][-len(jam):]==jam:

                                last_words.append(jam)
                                lis_res[j] = lis_res[j].replace(jam, '', 1)
 
                    lis_target_ind.append(i)

            data_t_after.append(data_t[i])
            data_w_jamo[i] = ''.join(lis_res)
            
        else:
            data_t_after.append(data_t[i])
            
    
    
        lis_normal = []
    
        for i in data_w_jamo:
            jam_n = Jamodealer(i)
            lis_normal.append(jam_n.make_one())
    
        
        
    for i in range(len(lis_target_ind)):
        if 'ㅅㅔㅇㅛ' == last_words[i] or 'ㄹㄹㅐㅇㅛ' == last_words[i]:
            
            for wk in dic.lis_wk:
                if data_w_jamo[lis_target_ind[i]][-len(wk[0])-1:-1] ==wk[0]:

                    ele = data_w_jamo[lis_target_ind[i]][:-len(wk[0])-1]
                    ele = ele + wk[1]
                    ele = ele + data_w_jamo[lis_target_ind[i]][-1]
                    data_w_jamo[lis_target_ind[i]] = ele
                    
                    break
        
    return data_w, data_t, lis_ind, data_w_jamo, data_t_after, last_words, lis_target_ind


########################## preprocessing with Khaiii ##########################

########################## preprocessing with Mecab ###########################

def prepro_ch03(input, lis_ef, tag_last, lis_w_last, lis_w_last_not, lis_ic):
    
    lis_res_word = []
    
    lis_input = input.split()
    lis_word = []
    lis_tag = []
    lis_last_word = []
    lis_ind = []
    
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
        
        jam_pre = Jamodealer(elem_w)
        lis_word.append(''.join(jam_pre.jamo))
        lis_tag.append(elem_t)
    
    for i in range(len(lis_tag)):
        
        if 'EF/SF' in lis_tag[i] or 'EF/SV' in lis_tag[i] or 'EF/SC' in lis_tag[i] or 'JX/SF' in lis_tag[i] or 'JX/SC' in lis_tag[i] or 'IC' in lis_tag[i] or 'IC' in lis_tag[i] or (('NP' in lis_tag[i] or 'NNG' in lis_tag[i]) and ('ㅈㅓ' in lis_word[i] or 'ㅈㅔ' in lis_word[i] or 'ㄷㅏㅇㅅㅣㄴ' in lis_word[i])):
            elemen_t = lis_tag[i].split('/')
            elemen_w = lis_word[i].split(' ')
            flag = 0
            
            
            for j in range(len(elemen_t)):

                flag_end = detect_h(elemen_w[j], lis_w_last_not, lis_w_last)
                
                
                if (flag_end == 1 and 'EF' in elemen_t[j]) or (flag_end == 1 and 'JX' in elemen_t[j]):
                    for jam in lis_w_last_not:
                        
                        if len(elemen_w[j])>=len(jam):
                            
                            if elemen_w[j][-len(jam):]==jam:
                                
                                
                                lis_ind.append(i)
                                lis_last_word.append(jam)
                                elemen_w[j] = elemen_w[j][:-len(jam)]
                                elemen_w[j] = elemen_w[j] + '__+__'
                                
                                break
                                
                ############# 인칭 대명사 변경 #############                
                ## 인칭 대명사를 사전에 미리 변경한다                
                elif (('NP' in lis_tag[i] or 'NNG' in lis_tag[i]) and ('ㅈㅓ' in lis_word[i] or 'ㅈㅔ' in lis_word[i] or 'ㄷㅏㅇㅅㅣㄴ' in lis_word[i])) or ('IC' in lis_tag[i] and('ㄴㅔ' in lis_word[i] or 'ㅇㅏㄴㅣㅇㅛ' in lis_word[i])):
                    
                    jam1 = Jamodealer(elemen_w)
                    s = jam1.make_one()

                    key_u = 0

                    ss = proc_khaiii_with_Tag(s)
                    tagt = ss[1].split('/')[:-1]
                    wordw = ss[0].split('/')[:-1]

                    for u in range(len(tagt)):
                        if tagt[u]=='NP':
                            if wordw[u]=='저' or wordw[u]=='제':
                                key_u = 1
                            elif wordw[u]=='당신':
                                key_u = 2
                        elif tagt[u]=='IC':
                            if wordw[u]=='네':
                                key_u = 3
                        elif tagt[u]=='VCN' or tagt[u]=='IC':
                            if wordw[u][:2]=='아니':
                                key_u = 4
            
                    flag = 0
                    for ind in range(len(elemen_t)):
                        if flag==0 and key_u>0:

                            if key_u == 1:

                                if elemen_t[ind][:2]=='NP' or elemen_t[ind][:3]=='NNG':
                                    
                                    if elemen_w[ind][:2] == 'ㅈㅓ':
                                        
                                        elemen_w[ind] = 'ㄴㅏ' + elemen_w[ind][2:]
                                        flag = 1

                                    elif elemen_w[ind][:2] == 'ㅈㅔ':

                                        elemen_w[ind] = 'ㄴㅐ' + elemen_w[ind][2:]
                                        flag = 1
                            
                            elif key_u==2:
                                if len(elemen_w[ind])>=6:
                                    if elemen_w[ind][:6] == 'ㄷㅏㅇㅅㅣㄴ':

                                        elemen_w[ind] = 'ㄴㅓ' + elemen_w[ind][6:]
                                        flag = 1
                                        if len(elemen_t)-1 >ind:
                                            if elemen_t[ind+1] == 'JX' or elemen_t[ind+1] == 'JKS' or elemen_t[ind+1] == 'JKO' or elemen_t[ind+1] == 'JKB':
                                                if elemen_w[ind+1] == 'ㅇㅡㄹ':
                                                    elemen_w[ind+1] = 'ㄹㅡㄹ'
                                                elif elemen_w[ind+1] == 'ㅇㅡㄴ':
                                                    elemen_w[ind+1] = 'ㄴㅡㄴ'
                                                elif elemen_w[ind+1] == 'ㅇㅣ':
                                                    elemen_w[ind+1] = 'ㄱㅏ'
                                                elif elemen_w[ind+1] == 'ㄱㅘ':
                                                    elemen_w[ind+1] = 'ㅇㅘ'
                                                    
                            elif key_u==3:
                                if len(elemen_t)>1:
                                    
                                    if elemen_t[1]=='SC' or elemen_t[1]=='SF':
                                        if elemen_w[ind][:2] == 'ㄴㅔ':
                                        
                                            elemen_w[ind] = 'ㅇㅡㅇ' + elemen_w[ind][2:]
                                            flag = 1
                            else:
                                if elemen_t[ind][:2] == 'IC':

                                    if elemen_w[ind][4:6] == 'ㅇㅛ':

                                        elemen_w[ind] = elemen_w[ind][:4] + elemen_w[ind][6:]

                                        flag = 1

                    
                                
            res_w = ''.join(elemen_w)
            lis_result.append(res_w)
                                
        else:
            
            rere = lis_word[i].split(' ')
            
            resres = ''.join(rere)
            
            lis_result.append(resres)
            
            
    return lis_result, lis_tag, lis_ind, lis_last_word

########################## preprocessing with Mecab ###########################

def treatSF(stc, ex):
    ind_point = -1
    point = ''
    if '__+__' in stc:
        ind_point = stc.index('__+__')
        stc = stc.replace('__+__', '', 1)
    
    r_word = ''
    r_pun = ''
    
    if ind_point!=-1:
        r_word = stc[:ind_point]
        r_pun = stc[ind_point:]
    else:
        r_word = stc
    return r_word+ex+r_pun

def delete_EP_si(stn, taglist):
    si = stn[-3:-1]
    eusi = stn[-5:-1]
    check_si = taglist[-11:-2]
    
    result =''
    flag = 0
    if taglist.find('SF') !=-1:
        if (eusi =='ㅇㅡㅅㅣ') and (check_si.find('EP+EP')!=-1 or check_si.find('EP/NULL')!=-1):
            result = stn[:-5]+stn[-1]
            flag = 1
        elif (si =='ㅅㅣ') and (check_si.find('/EP/')!=-1):

            result = stn[:-3]+stn[-1]


    return result, flag

def check_VV_VA(sentence, tag):

    tt = tag.split('/SF')
    t= tt[0][-6:]
    if 'VV' in t or 'VX' in t or 'XSV' in t or ('VV/EP' in tag and 'ㅅㅣ' in sentence[-5:-1]) :
        return 1
    elif 'VA' in t:
        return 0
    else:
        return -1
    
## 종결어미 자리를 뜻하는 문자를 없애는 함수. 어체 간 변환을 할 때 사용됨
def detach_endmark(sentence):
    endmark = sentence[-6:-1]

    if endmark == '__+__':
        sentence = sentence[:-6]+sentence[-1]
    else:
        endmark = -1
    return sentence, endmark

def attach_endmark(sentence):
    endmark = '__+__'
    sentence = sentence[:-1]+endmark+sentence[-1]
    return sentence

##if Verb & adjective
## '-시' 등 선어말 처리
## 습니다는 동사면 '는다', 그외에는 '다'로 간다
def rememberSpace_k(lis, input):
    
    rlis = []
    
    for i in range(len(lis)):
        if lis[i]==input:
            rlis.append(i)
            
    for i in range(len(rlis)):
        rlis[i] = rlis[i]-i      
    return rlis

def convertSpace_k(lis_space,lis_lis):
    
    rlis = []
    k=0
    for i in range(len(lis_lis)):
        
        if k in lis_space:
            rlis.append(i)
            
        k = k+len(lis_lis[i])
        

    return rlis

def proc_khaiii(input):
    
    r_sen = input
    
    res = ''
    slis = []
    for i in range(len(input)):
        if r_sen[i]==' ':
            slis.append(1)
        elif r_sen[i]=='  ':
            slis.append(2)
            
    wlis = r_sen.split(' ')
    
    uu = khai.analyze(wlis[0])
    
    elem = ''
    
    for data in uu[0].morphs:
        elem = elem + data.lex
    
    res = res+elem
    
    for i in range(len(slis)):
        elem = ''
        elem = elem+slis[i]*' '
        if i != len(wlis)-1:
            uu = khai.analyze(wlis[i+1])
            for data in uu[0].morphs:
                elem = elem+data.lex
        res = res+elem
    return res

def proc_khaiii_with_Tag(input):
    
    r_sen = input
    
    res1 = ''
    res2 =''
    slis = []
    for i in range(len(input)):
        if r_sen[i]==' ':
            slis.append(1)
        elif r_sen[i]=='  ':
            slis.append(2)
            
    wlis = r_sen.split(' ')
    
    uu = khai.analyze(wlis[0])
    
    elem = ''
    tag =''
    
    for data in uu[0].morphs:
        elem = elem + data.lex+'/'
        tag = tag+data.tag+'/'
    
    res1 = res1+elem
    res2 = res2+tag
    
    for i in range(len(slis)):
        elem = ''
        tag = ''
        elem = elem+slis[i]*' '
        if i != len(wlis)-1:
            uu = khai.analyze(wlis[i+1])
            for data in uu[0].morphs:
                elem = elem+data.lex+'/'
                tag = tag+data.tag+'/'
        res1 = res1+elem
        res2 = res2+tag
    return res1,res2
