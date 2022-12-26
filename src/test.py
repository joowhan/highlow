# -*- coding: utf-8 -*-
# © 2022 Joowhan Kim, Jaemu Heo, Jeonghui Kim <joy980721@gmail.com>
# Made by MILab in Handong Global University

from high2low import Changer_low as ch_low
import utils as util
#from low2high import Changer_high as ch_high
import is_horl as is_horl

txt = input("Enter Korean Sentence: ")
ch = ch_low()
#ch_high = ch_high()

hi = is_horl.isHigh()
detect=hi.isThisHigh(txt)

# 높임말
if detect ==1:
    hi.getState(detect)
    output = ch.processText(txt)
    print("Converted Result:", output)
# 반말
else:
    hi.getState(detect)
    output = util.tohigh(txt)
    print("Converted Result:", output)






