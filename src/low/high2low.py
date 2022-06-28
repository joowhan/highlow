import low_utils as util
import dictionary as dic

class Changer_low(object):
    
    def __init__(self):
        self.re_value=''
        
    def to_low(self, input):

        if '  ' in input:
            return input
        result = input

        converted_w, converted_t, target_ind ,last_ef = util.prepro_ch03(result, dic.lis_beta_ef, dic.lis_tag_last, dic.lis_end_2low, dic.lis_end, dic.lis_ic)


        if len(target_ind)!=0:

            for i in range(len(target_ind)):
                
                new_end = self.__make_end_low(converted_w[target_ind[i]], converted_t[target_ind[i]], last_ef[i])
                
                converted_w[target_ind[i]] = new_end
            
            res = ' '.join(converted_w)
            jam = util.Jamodealer(res)
            return jam.make_one()

        return input

    def __convertSpecialCase_AhOh(self, stc):
    ## 수정할 필요 있음!
    #danger
        sentence, endmark = util.detach_endmark(stc)
        if sentence[-3:-1] == 'ㅍㅡ' or sentence[-3:-1] == 'ㅃㅡ':
            if sentence[-5:-3].find('ㅏ') !=-1 or sentence[-5:-3].find('ㅗ')!=-1:
                return 'ㅏ'
            else:
                return 'ㅓ'
        elif sentence[-3:].find('ㅏ') !=-1 or sentence[-3:].find('ㅗ') !=-1:
            return 'ㅇㅏ'
        else:
            return 'ㅇㅓ'
        
    # 일부 주체 높임 어휘 처리
    def __treatFormal_vv(self, sentence):
        for key in dic.formal_vv:
            if sentence.find(key) !=-1:
                sentence = sentence.replace(key,dic.formal_vv[key])
        return sentence
    
    def __check_NoRule(self, stem,predicate):
        #this is temp function. Need to modify this function
        if predicate.find('ㅓ') !=-1:
            #print(stem+predicate)
            if (stem+predicate) =='ㄱㅡㄹㅓ':
                return 'ㅐ'
        else:
            return ''
    
    #'ㅇㅗㄹㅡ'
    def __convertSpecialCase_SaeYo(self, stc, ending, tag):
        result = ''
        end_EF=''
        final=''
        sentence, endmark = util.detach_endmark(stc)

        pun = sentence[-1:]
        predicate = sentence[-3:-1]
        stem = sentence[:-3]
        isVcp = tag[-12:]

        #만약 VCP가 있다면 '야'를 붙이고 return 한다.
        if isVcp.find('VCP/EP+EF') != -1 or isVcp.find('VCP+EP+EF') !=-1:
            final = 'ㅇㅑ'
            if endmark !=-1: # 문장에 __+__가 있었으면
                sentence = util.attach_endmark(sentence)
            converted = util.treatSF(sentence, final)
            return converted
        # 'ㄹ'규칙 활용
        elif predicate in dic.EF_R_rule:
            result= dic.EF_R_rule[predicate]
            ##'아' 또는 '어' 로 처리
            end_EF = self.convertSpecialCase_AhOh(sentence)
            final = result +end_EF
        #'르' 불규칙 활용
        elif predicate =='ㄹㅡ':
            # 용언 종성에 ㄹ이 있다면
            predicate = predicate.replace('ㄹㅡ','')
            sentence = stem+predicate + pun
            end_EF = self.convertSpecialCase_AhOh(sentence)
            end_EF = end_EF[-1]

            if sentence[-1].find('ㄹ') != -1:
                final = 'ㄹ'+end_EF
            else:
                final  = 'ㄹㄹ'+end_EF

        ##'우' 불규칙 활용
        # '푸'를 제외한 다른 'ㅜ'는 'ㅓ'와 결합
        elif predicate.find('ㅍㅜ') !=-1:
            predicate = predicate.replace('ㅜ','')
            sentence = stem+predicate + pun
            final = 'ㅓ'
        #'오' 불규칙 활용(현 버전에서는 고려하지 않음. It is not considered in the current version.)
        #'하' 불규칙 활용
        elif predicate.find('ㅎㅏ') !=-1:
            predicate = predicate.replace('ㅏ','')
            sentence = stem + predicate + pun
            final = 'ㅐ'
        #활용이 안되었던 용언 처리
        else:
            if predicate.find('ㅡ') !=-1:
                end_EF = self.convertSpecialCase_AhOh(sentence)
                predicate = predicate.replace('ㅡ','')
                sentence = stem + predicate + pun
                final = end_EF[-1]
            ## 수정할 필요 있음. (In the current version, there is a possibility of an error in the following part.)
            elif predicate.find('ㅗ') !=-1:
                predicate = predicate.replace('ㅗ','')
                sentence = stem+predicate+ pun
                final = 'ㅘ'
            elif predicate.find('ㅜ') !=-1:
                predicate = predicate.replace('ㅜ','') 
                sentence = stem + predicate+ pun
                final = 'ㅝ'
            elif predicate.find('ㅣ') !=-1:
                predicate = predicate.replace('ㅣ','')
                sentence = stem+predicate+ pun
                final = 'ㅕ'
            else:
                final = self.convertSpecialCase_AhOh(sentence)
                if  predicate.find('ㅏ') !=-1:
                    final = ''
                elif  predicate.find('ㅓ') !=-1:
                    final = self.check_NoRule(stem,predicate)
                    if final != '':
                        ind = sentence.rfind('ㅓ')
                        sentence = sentence[:ind]+sentence[ind+1:]
                elif  predicate.find('ㅐ') !=-1:
                    final = ''
    #                 return final, sentence
    #             return final, sentence
    #     return final, sentence
        if endmark !=-1: # 문장에 __+__가 있었으면
            sentence = util.attach_endmark(sentence)
        converted = util.treatSF(sentence, final)
        return converted

    def __convertSpecialCase_Da(self, stc, ending, taglist):
        sentence, endmark = util.detach_endmark(stc)
        final =''
        isEp = sentence[-2:-1]
        if (isEp == 'ㅆ' or sentence.find('ㅇㅏㄶ') !=-1)and (taglist.find('VV/EF') !=-1 or taglist.find('VX/EF') !=-1):
            final = 'ㄷㅏ'
        elif taglist.find('EP/EF') !=-1 or taglist.find('VA/EF') !=-1 or taglist.find('VX/EF') !=-1:
            final = 'ㄷㅏ'
        elif taglist.find('VV/EF') !=-1:
            final = 'ㄴㅡㄴㄷㅏ'
        elif taglist.find('VV') !=-1:
            final = 'ㄴㅡㄴㄷㅏ'
        if endmark !=-1: # 문장에 __+__가 있었으면
            sentence = util.attach_endmark(sentence)
        converted = util.treatSF(sentence, final)
        return converted

    def __convertSpecialCase_Nida(self, sentence, ending, taglist):
        #시가 있으면 ㄴ다를 붙인다. 
        #형용사, 서술격 조사일 경우 convertSpecialCase_SaeYo를 통해 변경한 다음, 아/어를 제거 후 다를 붙이고
        #동사일 경우 ㄴ다를 붙여서 해결한다. 
        predicate = util.check_VV_VA(sentence, taglist)
        #VV
        if predicate == 1:
            final = 'ㄴㄷㅏ'
            converted = util.treatSF(sentence, final)
        #VA
        #형용사의 경우, 세요를 거친 후 마지막을 붙인다면 이상해질 수 있다. 그냥 khaiii를 쓰는 것이 안전하다고 판단된다. 
        elif predicate == 0:
            final = 'ㄷㅏ'
            temp=util.treatSF(sentence,ending)
            jam1 = util.Jamodealer(temp)
            s = jam1.make_one()
            converted_kh = util.proc_khaiii(s)
            converted_kh = converted_kh.replace('ㅂ니다', '__+__')
            converted = util.treatSF(converted_kh, final)
        else:
            final = 'ㄷㅏ'
            converted = util.treatSF(sentence, final)
        return converted
    
    def __convertSpecialCase_Yo(self, stc, ending, tag):
        sentence, endmark = util.detach_endmark(stc)
        pun = sentence[-1:]
        predicate = sentence[-3:-1]
        stem = sentence[:-3]
        isVcp = tag[-11:]

        temp =''
        ni = 0
        after_si, ni = util.delete_EP_si(sentence, tag)
        if after_si != '':
            sentence = after_si
            after_si =''

        if isVcp.find('VCP') != -1:
            final = 'ㅇㅑ'
        #temporary condition(일시적으로 넣어둔 오류 문장 처리 기능 -> 에요)
        # elif sentence[-3:-1]=='ㅇㅔ':
        #     sentence = sentence[:-3]+pun
        #     final = 'ㅇㅑ'
        else:
            final = ''

        if endmark !=-1: # 문장에 __+__가 있었으면
            sentence = util.attach_endmark(sentence)

        converted = util.treatSF(sentence, final)
        return converted
    
    def __convertSpecialCase_NaYo(self, sentence, ending, taglist):
        final ='ㄴㅣ'
        if taglist.find('/VCP+EF/') !=-1:
            final='ㄴㅏㄴㅣ'
        converted = util.treatSF(sentence, final)
        return converted    

    
    def __convert_EF(self, sentence, taglist, ending):
        re_value =''
        temp =''
        ni = 0
        flag = 0
        
        #존칭 동사 또는 보조 동사를 파악하고 이를 변환 전에 미리 바꿔주어야 한다. 
        for key in dic.EF:
            if ending == key:
                flag = 1
                re_value = dic.EF[key]
                #나요, 으세요(으세요, 세요 모두 함수에서 커버 가능), 습니까 case
                if re_value == 'special0':
                    #시처리하기
                    after_si, ni = util.delete_EP_si(sentence, taglist)
                    if after_si != '':
                        sentence = after_si
                        after_si =''
                    temp = self.__convertSpecialCase_AhOh(sentence)
                    re_value = util.treatSF(sentence, temp)
                    #ㅗ,ㅜ 이면 ㅘ, ㅝ로 결합할 것
                #-세요,십니다, 십니까
                elif re_value == 'special1':
                    #시처리하기
                    after_si, ni = util.delete_EP_si(sentence, taglist)
                    if after_si != '':
                        sentence = after_si
                        after_si =''
                    re_value = self.__convertSpecialCase_SaeYo(sentence, ending, taglist)
                elif re_value == 'special2':
                    re_value = self.__convertSpecialCase_Da(sentence, ending, taglist)
                elif re_value == 'special3':
                    #시처리 안함 '시' 보존
                    re_value = self.__convertSpecialCase_Nida(sentence, ending, taglist)
                elif re_value == 'special4':
                    re_value = self.__convertSpecialCase_SaeYo(sentence, ending, taglist)
                    #print(re_value)
                    if ending == 'ㅇㅡㅂㅅㅣㄷㅏ':
                        temp = self.__convertSpecialCase_AhOh(sentence)
                        re_value = util.treatSF(sentence, temp)
                elif re_value == 'special5':
                    re_value = self.__convertSpecialCase_Yo(sentence, ending, taglist)
                elif re_value == 'special6':
                    re_value = self.__convertSpecialCase_NaYo(sentence, ending, taglist)
                else:
                    #위험하기 때문에 데이터 확인 후 수정(보류)
#                     if taglist.find('EP') !=-1 and sentence[-4:].find('ㅅㅣ.'):
#                         sentence = delete_EP_si(sentence, taglist)
#                         re_value = convertSpecialCase_SaeYo(sentence, ending)
#                     else:
#                         re_value = treatSF(sentence,re_value)
                    re_value = util.treatSF(sentence,re_value)
        if flag ==0:
            return util.treatSF(sentence, ending)
        return re_value
    
    def __convert_IC(self, sentence, taglist, ending):
        
        re_value = ''
        flag = 0
        for key in dic.IC:
            if ending == key:
                re_value = dic.IC[key]
                flag = 1
        if flag != 1:
            re_value = ending
        re_value = util.treatSF(re_value, sentence)
        return re_value
    
    def __make_end_low(self, sentence, taglist, ending):
        re_value =''
        sentence = self.__treatFormal_vv(sentence)
        if taglist.find('IC') !=-1 and len(taglist)<6:
             re_value = self.__convert_IC(sentence, taglist, ending)
        else:
            re_value = self.__convert_EF(sentence, taglist, ending)
        return re_value
    
    
    
    

    def processText(self,stc):
        result = stc
        flag = 0
        if result[-1]=='\n':
            result = result.replace('\n','')   
        num = 0
        while 1:
            if result[-1-num]!=' ':
                break
            else:
                num = num+1
                
        if num==0:
            rere = result
        else:
            rere = result[:-num]
            
        
        r_pun = ''
        r_word = rere
        while True:
            if r_word[-1] in dic.SV_LIST:
                r_pun = r_pun+r_word[-1]
                r_word = r_word[:-1]
            else:
                break
        
        num_space = 0
        for i in r_word:
            if i==' ':
                num_space = num_space+1
            else:
                break
            
        if num_space!=0:
            r_word = r_word[num_space:]

        plus = ''
        for s in range(num_space):
            plus = plus+' '
    
        if r_word[-1] =='?' or r_word[-1] =='.' or r_word[-1] =='!' or r_word[-1] =='\"':
            r_word = r_word
        else:
            r_word = r_word+'.'
            flag = 1

        res = self.to_low(r_word)
##########For data extraction##########
#         try:
#             res = self.to_low(r_word)
#         except:
#             print('exception sentece number: ', count)
#             res = r_word
##########For data extraction##########

        r_word = plus+r_word
        res = plus+res
        
        if flag ==1:
            res = res[:-1]

        return res+r_pun[::-1]