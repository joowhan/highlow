from high2low import Changer_low as ch_low
import is_horl as is_horl
#from isHighlow import Checker_hl as checker

txt = input("Enter Korean Sentence: ")

hi = is_horl.isHigh()
detect=hi.isThisHigh(txt)
hi.getState(detect)    
ch = ch_low()

output = ch.processText(txt)
print("Converted Result:", output)


