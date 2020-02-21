#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: xiezuoru
### 调用GET方法，读取A0号引脚的电平。
在该案例中可以修改的参数有:
    - url:设置成虚谷号的IP地址
    - pin:对应的引脚 A0-A5，D0-D13 
注意：该方法需要外接传感器，否则数字口默认返回为低电平，模拟口返回随机数。
"""
import requests

vvboardip='192.168.3.42'
pin='D13'
value=1
t=1
payload = {"pin":pin,'value':value,'type':t}
re = requests.post(url='http://'+ vvboardip +':1024/',params=payload) 
if (re.status_code==200):
    r=re.json()
    print('成功发送控制命令：'+ r["msg"]) 
    print('返回的信息为：') 
    print(re.text) 