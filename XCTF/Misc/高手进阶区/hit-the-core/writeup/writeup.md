# hit-the-core

1. `strings`发现一个长字符串：  
cvqAeqacLtqazEigwiXobxrCrtuiTzahfFreqc{bnjrKwgk83kgd43j85ePgb_e_rwqr7fvbmHjklo3tews_hmkogooyf0vbnk0ii87Drfgh_n kiwutfb0ghk9ro987k5tfb_hjiouo087ptfcv}

2. 把大写提取出来为ALEXCTF，规律是字母间间隔为5  

3. 写脚本提取
```python
s = 'cvqAeqacLtqazEigwiXobxrCrtuiTzahfFreqc{bnjrKwgk83kgd43j85ePgb_e_rwqr7fvbmHjklo3tews_hmkogooyf0vbnk0ii87Drfgh_n kiwutfb0ghk9ro987k5tfb_hjiouo087ptfcv}'

flag = ''

for i in range(3, len(s), 5):
    flag += s[i]

print(flag)
```
