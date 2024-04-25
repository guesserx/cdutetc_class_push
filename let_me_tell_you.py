import time
import json
import random


def generate_code(long) :
    numbers = '1234567890'
    code = ''
    for i in range(long) :
        code += random.choice(numbers)
    return code


def return_code(long) :
    code = generate_code(long)
    f = open('let-me-tell.json', 'r', encoding='utf-8')
    datas = json.load(f)  # 如果没有一个初始数据会出错
    for data in datas :
        if code == data['get_code'] :
            generate_code(long)
    return code


def tell_me(message,user,nickname):
    time_now = time.strftime("%I:%M:%S")
    code = return_code(6)
    f = open('let-me-tell.json', 'r', encoding='utf-8')
    datas = json.load(f)
    data = {"message": message, "time": time_now,"user":user,"nickname":nickname,"get_code":code}
    datas.append(data)
    f = open('let-me-tell.json', 'w', encoding='utf-8')
    f.write(json.dumps(datas))
    f.close()
    return code


def tell_you(code):
    f = open('let-me-tell.json', 'r', encoding='utf-8')
    datas = json.load(f)
    for data in datas:
        if data['get_code'] == code:
            f.close()
            return data['nickname'], data['message'],data['time']
    return None,None,None
