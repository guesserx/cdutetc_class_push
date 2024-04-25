import json
from datetime import datetime
import math
# import time
# import os
# os.environ['TZ'] = 'Asia/Shanghai'
# time.tzset()
# 如果你的服务器为海外服务器，请取消注释上诉设置时区，选中区块后，按ctrl+/批量取消

week_list={'0':'星期一',
           '1':'星期二',
           '2':'星期三',
           '3':'星期四',
           '4':'星期五',
           '5':'星期六',
           '6':'星期天',
          '-1':'星期天'
}

class_time_list={'1-2节':['8,15,0','9,0,0','9,15,0','9,50,0'],
                 '3-4节':['10,5,0','10,50,0','10,55,0','11,40,0'],
                 '5-6节': ['14,30,0', '15,15,0', '15,20,0', '16,05,0'],
                 '7-8节': ['16,20,0', '17,05,0','17,10,0', '17,55,0' ],
                 '9-10节': ['19,10,0', '19,55,0', '20,0,0','20,45,0']
                 }

def convert_to_minutes(time_str):
    #print(time_str)
    hour, minute, _ = map(int, time_str.split(','))
    return hour * 60 + minute


def is_time_in_range(current_time, start_time, end_time):
    return start_time <= current_time <= end_time



def check_current_time():
    now = datetime.now()
    current_minutes = (now.hour) * 60 + now.minute + 20
    for period, time_range in class_time_list.items():
        start_time = convert_to_minutes(time_range[0])
        end_time = convert_to_minutes(time_range[3])
        if is_time_in_range(current_minutes, start_time, end_time):
            return period
    return None


def cn_week_name(today_week) :
    if today_week in week_list :
        return week_list[today_week]
    else :
        return today_week

def fun(type) :
    if type == 0 :return return_now_class()
    elif type == 1 :return return_today_class()
    else:return "参数错误"


def check_week(weeks):
    for week in weeks.split(',') :
        if '-' in week and '双' not in week and '单' not in week :
            begin_week, end_week = map(int, week.split('-'))
            if begin_week <= current_week and current_week <= end_week :
                return True
        elif '双' in week :
            week = week.replace('双','')
            begin_week, end_week = map(int, week.split('-'))
            for i in range(begin_week, end_week+1) :
                if i==current_week and i/2==0:
                    return True
        elif '单' in week :
            week = week.replace('单','')
            begin_week, end_week = map(int, week.split('-'))
            for i in range(begin_week, end_week+1) :
                if i==current_week and i/2!=0:
                    return True
        else :
            if int(week) == current_week :
                return True
    return False


today_week=cn_week_name(str(datetime.today().weekday()))
f = open('kblist.json','r',encoding='utf-8')
f = json.load(f)
days = (datetime.strptime(str(datetime.now().year)+'-'+str(datetime.now().month)+'-'+str(datetime.now().day),'%Y-%m-%d') - datetime.strptime("2024-03-01", "%Y-%m-%d")).days
current_week = math.ceil((days+5)/7)#开头有4天，今天没算进去，一共加5


def check_add_week(weeks,days_add):
    next_days_week = math.ceil((days + 5 +days_add) / 7)
    #print(next_days_week)
    for week in weeks.split(',') :
        if '-' in week and '双' not in week and '单' not in week :
            begin_week, end_week = map(int, week.split('-'))
            if begin_week <= next_days_week and next_days_week <= end_week :
                return True
        elif '双' in week :
            week = week.replace('双','')
            begin_week, end_week = map(int, week.split('-'))
            for i in range(begin_week, end_week+1) :
                if i==next_days_week and i/2==0:
                    return True
        elif '单' in week :
            week = week.replace('单','')
            begin_week, end_week = map(int, week.split('-'))
            for i in range(begin_week, end_week+1) :
                if i==next_days_week and i/2!=0:
                    return True
        else :
            if int(week) == next_days_week :
                return True
    return False


def next_days(days_add) :
    today_week = cn_week_name(str((datetime.today().weekday()+1+days_add)%7-1))
    print(today_week)
    has_class = False
    kc=[]
    cd=[]
    jc=[]
    class_time=[]
    for w in f['kbList'] :
        if today_week == w['xqjmc']:
            #print(w,'\n========')
            w['zcd'] = w['zcd'].replace('(', '').replace(')', '').replace('周', '')
            if check_add_week(w['zcd'], days_add) :
                kc.append(w['kcmc'])
                cd.append(w['cdmc'])
                jc.append(w['jc'])
                if w['zcd'] not in class_time_list.keys() :
                    #print(w['jc'])
                    class_time.append(unmentioned_class_time_keys(w['jc']))
                else :
                    class_time.append(class_time_list[str(w['jc'])])
                has_class=True
    if has_class :
        return kc,cd,jc,class_time
    else :
        return f'{days_add}日后无课','无','无','无'


def return_now_class() :
    for w in f['kbList'] :
        if today_week == w['xqjmc'] and check_current_time() == w['jc']:
            #！！！！！！这里可能有问题，列表中没有提到的节数会不返回课程！！！！！！
            #TODO：此问题可能不会被修复
            w['zcd'] = w['zcd'].replace('(', '').replace(')', '').replace('周', '')
            if check_week(w['zcd']) :
                is_class=False
                return w['kcmc'],w['cdmc'],w['jc'],class_time_list[str(w['jc'])]
    return '当前无课','无','无','无'

def today_next_class() :
    names, rooms, class_times, class_time_ns = return_today_class()
    i = 0
    now = datetime.now()
    current_time = (now.hour)*60 + now.minute
    if '今日无课' not in str(names):
        for class_time_n in class_time_ns:
            #print(class_time_n)
            if convert_to_minutes(class_time_n[0]) >=current_time:
                return names[i],rooms[i],class_times[i],class_time_n
            #print(convert_to_minutes(class_time_n[0]),current_time)
            i += 1
    return '无最近课程', '无', '无', '无'


def unmentioned_class_time_keys(jc) :
    start , end = map(int, jc.replace('节','').split('-'))
    start_time = '0'
    end_time = '0'
    for key in class_time_list.keys() :
        list_start , list_end = map(int, key.replace('节','').split('-'))
        if list_start == start :
            start_time = class_time_list[key]
            continue
        if list_end == end :
            end_time = class_time_list[key]
            break
    return str(start_time)+str(end_time)


def return_today_class() :
    has_class = False
    kc=[]
    cd=[]
    jc=[]
    class_time=[]
    for w in f['kbList'] :
        if today_week == w['xqjmc']:
            #print(today_week)
            w['zcd'] = w['zcd'].replace('(', '').replace(')', '').replace('周', '')
            if check_week(w['zcd']) :
                kc.append(w['kcmc'])
                cd.append(w['cdmc'])
                jc.append(w['jc'])
                if w['jc'] not in class_time_list.keys():
                    class_time.append(unmentioned_class_time_keys(w['jc']))
                else:
                    class_time.append(class_time_list[str(w['jc'])])
                has_class=True
    if has_class :
        return kc,cd,jc,class_time
    else :
        return '今日无课','无','无','无'
