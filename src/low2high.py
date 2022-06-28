# -*- coding: utf-8 -*-

import hangul
import utils as util
import dictionary as dic
from khaiii import KhaiiiApi
khai = KhaiiiApi()

class Changer_high:
    
    def tohigh(self,input):

        result = []

        analyzed = api.analyze(input)  
        for data in analyzed:
            lis_word = []
            lis_tag = []
            for morph in data.morphs:
                lis_word.append(morph.lex)
                lis_tag.append(morph.tag)
    #         print(lis_word)
    #         print(lis_tag)
    #         print("====================")
            try:
                lis_tag.index('EF')
                result.append(to_high(data.lex,lis_word,lis_tag))
            except:
                if len(lis_tag) == 2 and lis_tag[0] == "NP" and ("JK" in lis_tag[1] or "JX" == lis_tag[1]):
    #                 print(lis_word)
                    if lis_word[0] == "나":
                        lis_word[0] = "저"
                        if lis_word[1] == "ㄴ":
                            result.append("전")
                        elif lis_word[1] == "ㄹ":
                            result.append("절")
                        else:
                            result.append(''.join(lis_word))
                    elif lis_word[0] == "너":
                        lis_word[0] = "당신"
                        if lis_word[1] == "ㄴ":
                            result.append("당신은")
                        elif lis_word[1] == "ㄹ":
                            result.append("당신을")
                        elif lis_word[1] == "랑":
                            result.append("당신과")
                        else:
                            if lis_word[1] == "는":
                                lis_word[1] = "은"
                            elif lis_word[1] == "와":
                                lis_word[1] == "과"
                            elif lis_word[1] == "가":
                                lis_word[1] = "이"
    #                             print(lis_word[1])
                            elif lis_word[1] == "를":
                                lis_word[1] = "을"
                            result.append(''.join(lis_word))
                    elif data.lex == "내가":
                        result.append("제가")
                    elif data.lex == "네가":
                        result.append("당신이")
                    else:
                        result.append(data.lex)
                else:
                    result.append(data.lex)

        return ' '.join(result)
        

    
    
    def to_high(self, result, lis_word, lis_tag):
    #     print(lis_word)
    #     print(lis_tag)
        EF_indexs = [pos for pos, char in enumerate(lis_tag) if char == "EF"]
        EF_index = EF_indexs[-1]
        EF = lis_word[EF_index]
        EF_next = lis_word[EF_index+1]
        EF_front = lis_word[EF_index-1]
        if hangul.is_hangul(EF_next):
            return result
        #다로 끝나는 친구들
        if EF in da_case1:
            result = result.replace('다'+EF_next, '입니다'+EF_next)
        elif EF in da_case2:
            if EF == 'ㄴ다':
                result = hangul.join_jamos(hangul.split_syllables(result).replace('ㄴㄷㅏ_'+EF_next, 'ㅂㄴㅣ_ㄷㅏ_' + EF_next))
            else:
                jamo = hangul.split_syllables(EF[:-1])[-1]
                result = hangul.join_jamos(hangul.split_syllables(result).replace(jamo + 'ㄷㅏ_' + EF_next, 'ㅂㄴㅣ_ㄷㅏ_' + EF_next))
        elif EF in da_case3:
            if '는다' in EF:
                result = result.replace('는다'+EF_next, '습니다'+EF_next)
            else:
                result = result.replace('다'+EF_next, '습니다'+EF_next)
        elif EF == '다':
            if lis_tag[EF_index-1] in da_tag_case1:
                result = result.replace('다'+EF_next, '입니다'+EF_next)
            elif lis_tag[EF_index-1] in da_tag_case2:
                jamo = hangul.split_syllables(EF_front)[-1]
    #             print(jamo)
                #받침없는 경우(ㄹ,ㄴ포함)
                if jamo == '_' or jamo == 'ㄹ' or jamo == 'ㄴ' :
                    if (lis_tag[EF_index-1] == 'VCP' and lis_word[EF_index-1] == '이') and lis_word[EF_index-1] != result[result.rfind('다'+EF_next)-1]:
                        result = result.replace('다'+EF_next, '입니다'+EF_next)
                    else:
                        result = hangul.join_jamos(hangul.split_syllables(result).replace(jamo+'ㄷㅏ_'+EF_next, 'ㅂㄴㅣ_ㄷㅏ_' + EF_next))
                #받침있는 경우
                else:
                    result = result.replace('다'+EF_next, '습니다'+EF_next)
        #요로 끝나는 친구들 
        elif EF in yoo_low:
            if len(EF) == 1:
                if lis_word[-2] == EF and (lis_word[-2] == '어' or lis_word[-2] == "여") and lis_word[-2] != result[-2]:
                    result = result.replace(EF_next, '요'+EF_next)
                else:
                    result = result.replace(EF+EF_next, EF+'요'+EF_next)

            else:
                result = hangul.join_jamos(hangul.split_syllables(result).replace(hangul.split_syllables(EF[1:])+EF_next, hangul.split_syllables(EF[1:]+'요')+EF_next))
        #아
        elif EF == '아':
            if EF_front in ah_low:
    #             print(lis_word)
    #             print(lis_tag)
                result = result.replace(EF_next, '요'+EF_next)
        #구나
        elif '구나' in EF:
            result = result.replace(EF+EF_next, '네요'+EF_next)
        #야
        elif EF == '야':
            result = result.replace(EF+EF_next, '에요'+EF_next)
        #니 냐 느냐 는가
        elif EF == '니' or EF == '냐' or EF == '느냐' or EF == '는가':
            result = result.replace(EF+EF_next, '나요'+EF_next)
        #자
        elif EF == '자':
            result = result.replace(EF+EF_next, '지요'+EF_next)
        #라
        elif EF == '라':
            jamo = hangul.split_syllables(EF_front)[-1]
            if lis_tag[EF_index-1] == 'VX' or 'XSV':
                if jamo == '_':
                    result = result.replace(EF+EF_next, '세요'+EF_next)
                elif EF_front[-1] =='달':
                    result = result.replace(EF_front[-1]+EF+EF_next,'주세요'+EF_next)
                else:
                    result = result.replace(EF+EF_next, EF+'요'+EF_next)
        #아라, 어라
        elif EF == '아라' or EF == '어라':
            jamo = hangul.split_syllables(EF_front)[-1]
            check = result.find(EF_front+EF+EF_next)
            if check != -1:
                if jamo == 'ㄹ':
                    result = result.replace(EF_front+EF+EF_next, hangul.join_jamos(hangul.split_syllables(EF_front)[:-1])+'세요'+EF_next)
                elif jamo == '_':
                    result = result.replace(EF_front+EF+EF_next, EF_front+'세요'+EF_next)
                else:
                    result = result.replace(EF_front+EF+EF_next, EF_front+'으세요'+EF_next)
            else:
                ra_index = result.find('라'+EF_next)
                if result[ra_index-1:ra_index+1]=='라라':
                    result = result[:ra_index-len(EF_front)-1] + hangul.join_jamos(hangul.split_syllables(EF_front)[:-1])+'르세요' + result[ra_index+1:]
                elif jamo == 'ㄹ':
                    result = result[:ra_index-len(EF_front)] + hangul.join_jamos(hangul.split_syllables(EF_front)[:-1])+'세요' + result[ra_index+1:]
                elif jamo == '_':
                    result = result[:ra_index-len(EF_front)] + EF_front + '세요' + result[ra_index+1:]
                else:
                    result = result[:ra_index-len(EF_front)] + EF_front + '으세요' + result[ra_index+1:]
        elif EF == '더라' or EF == "다더라":
            result = result.replace(EF+EF_next, EF+'고요'+EF_next)
        elif EF == "잖니":
            result = result.replace(EF+EF_next, EF[0]+'아요'+EF_next)
        elif EF == "야지":
            result = result.replace(EF+EF_next, EF[0]+'죠'+EF_next)
        elif EF == "자아":
            result = result.replace(EF_front + EF[0] + EF_next, '지냅시다'+EF_next)
        elif EF == "이다":
            result = result.replace(EF+EF_next, "입니다" + EF_next)



        return result