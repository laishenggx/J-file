"""
#################################################################################################
分钟观测数据文件（J文件）内容读取的Python3程序.

•Coder: Lai Sheng @ College of Atmospheric Science ,Chengdu University of Information Technology.
•E-mail: laish12@lzu.edu.cn

目前只做了降水的读取，需要更改的就是sta_id、year、month。

-- Datas Output --
    pre_data: [Array] 维数为(当月日数,24,60)

#################################################################################################
"""

import numpy as np
import datetime as dt
from dateutil.rrule import *
from dateutil.relativedelta import relativedelta
import re

sta_id=54428
year=2016
month=7
dl='J%5d-%4d%02d.TXT'%(sta_id,year,month)
f=open(dl,'r')

def time_arranger(year,month):
    ini_time=dt.datetime(year,month,1,20,1)
    bg_time=ini_time+relativedelta(days=-1)
    ed_time=ini_time+relativedelta(months=+1)
    ed_time += relativedelta(days=-1)
    day = list(rrule(DAILY, dtstart=bg_time, until=ed_time, interval=1))
    ed_time += relativedelta(minutes=-1)
    time_list=list(rrule(MINUTELY,dtstart=bg_time,until=ed_time,interval=1))
    time_list=np.array(time_list)
    time_array=time_list.reshape((len(day)-1,24,60))
    data_store_array=np.zeros((len(day)-1,24,60))
    return time_array,data_store_array

def pre_data_trans(block):
    temp=[]
    block=re.findall('.{2}',block)
    for i in block:
        if i=='//':
            temp.append(np.nan)
        else:
            temp.append(int(i)*0.1)
    return np.array(temp)

file_content=[]
for ll in f:
    ll = ll.rstrip('\n')
    ll = ll.split(' ')
    if '' in ll:
        ll.remove('')
    file_content.append(ll)
f.close()

pre_flag=False
day=0
hour=0
for i in file_content:
    if i[0]=='R0':
        time,pre_data=time_arranger(year,month)
        pre_flag=True
    if i[0][-1]=='=':
        pre_flag = False
    if pre_flag and i[0][-1]=='.':
        if len(i[0])==1:
            pass
        elif i[0]=='/.':
            pre_data[day,:,:]=np.nan
        else:
            temp=pre_data_trans(i[0])
            pre_data[day,hour,:len(temp)]=temp
        day+=1
        hour=0
    if pre_flag and i[0][-1] == ',':
        if len(i[0])==1:
            pass
        elif i[0]=='/,':
            pre_data[day, hour, :] = np.nan
        else:
            temp=pre_data_trans(i[0])
            pre_data[day,hour,:len(temp)]=temp
        hour+=1
