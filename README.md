# **높임말 반말 변환 모듈**
edited this page on 29 Jun 2022<br>
© 2022 milab <joy980721@gmail.com>


### **Made by MILab*
**************
## 1. 변환의 기본 원리
다른 언어와 구별되게 한국어에는 높임 표현에 체계가 존재합니다. 이는 한국어의 대표적인 언어적 특성이라고 볼 수 있습니다. 본 프로젝트에서는 한국어의 상대높임법에 근거해, 일부 형태소를 변경해 높임말 반말 어체 변환을 시도하였습니다. 상대높임법은 국어의 높임법 중 가장 발달한 높임법으로, 듣는 사람을 높이거나, 낮추는 방법이며 이는 주로 종결어미에서 실현이 됩니다. 따라서 대화체를 기준으로 어체가 변환이 됩니다. 종결어미가 기준으로 어체가 변환되며, 부가적으로 인칭 대명사와 감탄사도 일부 표현은 변경되도록 구현되었습니다. 어체 간 변환은 격식체와 비격식체 내부에서 각각 변경되게 됩니다. 한국어 특성 상 예외적으로 바뀌지 않는 부분도 일부 존재하지만, 대부분의 경우, 위의 규칙을 따르게 됩니다. 

## 2. Getting Started
### - **Install**
#### * **형태소 분석기 설치**
먼저 형태소 분석기를 설치해야 합니다.
현 변환 모듈에서는 Mecab과 Khaiii 두 개의 형태소 분석기를 사용합니다. 두가지의 형태소 분석기 모두 설치해야 코드가 정상적으로 작동됩니다. <br>
>   #### **Mecab 설치 방법(Mac)**
> brew home도 설치가 되어 있어야 합니다.
> ```Shell
> $ pip install konlpy
> $ bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
>```

>#### **Mecab 설치 방법(Window)**
> 참고링크: [window에서 설치 참고 블로그](https://velog.io/@jyong0719/konlpy-mecab-%EC%84%A4%EC%B9%98-window)

>#### **khaiii 설치 방법(Mac)**
> 참고 링크: [khaiii Github](https://github.com/kakao/khaiii/wiki/%EB%B9%8C%EB%93%9C-%EB%B0%8F-%EC%84%A4%EC%B9%98)

형태소 분석기를 설치했다면, 다음은 hangul_utils를 설치해주어야 합니다. 
>#### **hangul-utils 설치**
> ```Shell
> pip install hangul-utils
>```

그 외에도 numpy, matplotlib, tqdm 등 설치를 해야 합니다.
(해당 문서에서 언급되지 않았던 API를 설치해야 할 수도 있습니다.)

#### * **변환 모듈 github**
현재는 모듈이 github에만 올라가 있는 상태이기 때문에 github에서 clone해서 사용할 수 있습니다. 
```shell
git clone https://github.com/joowhan/highlow.git
```

### - **Usages**
성공적으로 설치가 되었다면, 해당 모듈을 사용할 준비가 되었습니다. 이제 해당 모듈을 설치합니다.
github에서 코드를 가져오거나, 배포된 모듈을 설치할 수 있습니다. 먼저 사용하고자 하는 모듈을 import한 다음 변환 함수를 부르면 됩니다.

* **높임말, 반말 확인**
```python
import is_horl as is_horl
#높임말 판별 class 호출
hi = is_horl.isHigh()
#높임말이면 1, 반말이면 0으로 반환되는 함수입니다. 
detect = hi.isThisHigh(txt)
#getState()로 해당하는 상태를 출력할 수 있습니다.
hi.getState(detect)  

-> "다음 문장은 높임말입니다. 문장을 반말로 변경합니다."

```

* **높임말을 반말로 변환** <br>
반말로의 변환 과정은 고려해야 할 문법적 요소가 많으며 다소 복잡한 과정을 거칩니다. class를 호출해서, method를 호출해서 사용할 수 있습니다. 
```python
from high2low import Changer_low as ch_low
ch = ch_low()

txt = input("Enter Korean Sentence: ")
output = ch.processText(txt)
print("Converted Result:", output)
```

* **반말을 높임말로 변환** <br>
높임말로 변환은 khaiii 형태소 분석기가 사용되었으며, 간단하게 함수 호출로 변환이 가능합니다.
```python
    output = util.tohigh(txt)
    print("Converted Result:", output)
```

## 3. Structure
- src
  - dictionary.py: 어체 변환시 필요한 종결어미, 형태소 등의 dictionary
  - hagul.py
  - high2low.py: 높임말을 반말로 변경하는 class
  - is_horl.py: 높임말 반말 판단 class
  - low2high.py: 반말을 높임말로 변환하는 class(not use this project)
  - utils.py: 변환 시 필요한 method set
  - test.py: 사용 예시
- jupyter
  - low2high.ipynb
  - high2low.ipynb
  - hangul.py
## 4. Precautions
형태소 기반으로 변환이 되기 때문에, 입력하는 문장이 문법적으로 정확하지 않으면 제대로 분석이 되지 않아 변환이 안됩니다. 문장이 문법적으로 맞더라도, 형태소 분석기 역시 완벽하지 못해, 종종 제대로 분석을 못하는 경우가 존재합니다. 이 경우 역시 제대로 변환이 안될 수 있습니다. 
