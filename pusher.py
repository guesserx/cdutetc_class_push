from flask import Flask, request, make_response
import hashlib
import time
import xml.etree.ElementTree as ET
import saerch_self
import let_me_tell_you
import classls

app = Flask(__name__)

# 定义 TOKEN
TOKEN = "这个是微信公众号的token"


@app.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 微信服务器验证签名
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')

        if verify_signature(signature, timestamp, nonce):
            return echostr
        else:
            return 'Invalid Signature'
    elif request.method == 'POST':
        # 处理接收到的消息
        xml_data = request.data
        root = ET.fromstring(xml_data)
        msg_type = root.findtext('MsgType')

        if msg_type == 'event' and root.findtext('Event') == 'subscribe':
            # 处理关注事件
            response_xml = handle_subscribe_event(root)
        elif msg_type == 'text':
            # 处理文本消息
            response_xml = handle_text_message(root)
        else:
            response_xml = ""

        # 构造响应
        response = make_response(response_xml)
        response.headers['Content-Type'] = 'application/xml'
        return response


def verify_signature(signature, timestamp, nonce):
    # 验证消息签名
    tmpArr = [TOKEN, timestamp, nonce]
    tmpArr.sort()
    tmpStr = ''.join(tmpArr)
    hashed_str = hashlib.sha1(tmpStr.encode()).hexdigest()
    return hashed_str == signature


def handle_subscribe_event(xml):
    # 处理关注事件
    to_user_name = xml.findtext('FromUserName')
    from_user_name = xml.findtext('ToUserName')
    create_time = str(int(time.time()))
    msg_type = 'text'
    content = '🎉欢迎光临！小部分测试阶段仅供邀请用户使用，期间出现问题请及时报告，对此造成的不便还请海涵！'

    response_xml = f"""
        <xml>
            <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[{msg_type}]]></MsgType>
            <Content><![CDATA[{content}]]></Content>
        </xml>
    """
    return response_xml


def handle_text_message(xml):
    content = xml.findtext('Content').strip()
    if '/now' in content:
        name, room, class_time, class_time_n = saerch_self.fun(0)
        response_content = f'📖课程：{name}\n⛪︎教室：{room}\n节数：{class_time}\n上课时间 ：{class_time_n}'
    elif '/help' in content:
        response_content = """
📖 /now: 获取当前时间段的课程
⛪︎ /update: 更新课程表
📖 /today_all: 获取今天所有的课程信息
⛪︎ /next_class: 获取最近的下一节课信息
📖 /next 正整数: 获取未来几天的课程信息
⛪︎ openid: 获取openid
📖 /send 昵称@内容: 发送消息
⛪︎ /receive 六位纯数字取回码: 接收消息
📖 +, -, *, /等运算符: 计算表达式的值
"""
    elif '/update' in content:
        response_content = classls.get_new()
    elif '你好' in content and '/' not in content:
        response_content = "你好！服务器在香港热情地问候您！"
    elif '/today_all' in content:
        names, rooms, class_times, class_time_ns = saerch_self.fun(1)
        final_content = ''
        i = 0
        if '今日无课' not in str(names):
            for name in names:
                final_content += f'📖课程：{name}\n⛪︎教室：{rooms[i]}\n节数：{class_times[i]}\n上课时间 ：{class_time_ns[i]}\n====\n'
                i += 1
            response_content = final_content
        else:
            response_content = '今日无课'
    elif '/next_class' in content :
        name, room, class_time, class_time_n = saerch_self.today_next_class()
        response_content = f'📖课程：{name}\n⛪︎教室：{room}\n节数：{class_time}\n上课时间 ：{class_time_n}'
    elif '/next' in content:
        days_add = content.replace('/next ', '')
        if days_add.isdigit() == False:
            response_content = ('用法：/next 正整数')
        else:
            days_add = int(days_add)
            names, rooms, class_times, class_time_ns = saerch_self.next_days(days_add)
            final_content = ''
            i = 0
            if '后无课' not in str(names):
                for name in names:
                    final_content += f'📖课程：{name}\n⛪︎教室：{rooms[i]}\n节数：{class_times[i]}\n上课时间 ：{class_time_ns[i]}\n====\n'
                    i += 1
                response_content = final_content
            else:
                response_content = f'{days_add}日后无课'
    elif 'openid' in content :
        response_content = xml.findtext('FromUserName')
    elif '/send' in content :
        messages = content.replace('/send ','')
        if '@' not in messages:
            response_content = '用法：/send 昵称@内容'
        else :
            message = messages.split('@')
            openid = xml.findtext('FromUserName')
            response_content = f'消息取回码：{let_me_tell_you.tell_me(message[0],openid,message[1])}'
    elif '/receive' in content :
        code = content.replace('/receive ', '')
        if code.isdigit() == False:
            response_content = ('用法：/receive 六位纯数字取回码')
        else :
            message,nickname,send_time = let_me_tell_you.tell_you(str(code))
            if nickname != None:
                response_content = f'名称：{nickname}\n内容：{message}\n时间{send_time}'
            else :
                response_content = '取回码错误，请检查是否为6位纯数字'
    elif '+' in content or '-' in content or '*' in content or '/' in content:
        can_goon = True
        can_list = ['+','-','/','//','%','**','=','+=','-=','=','/=','%=','**=','&','|','<<','>','<','==','!=','>=','<=','*']
        if len(content)>=3 :
            for letter in content :
                if letter.isdigit() == False and letter not in can_list :
                    can_goon = False
                    break
        else :
            can_goon = False
        if can_goon :
            res = eval(content)
            response_content = f'计算结果：{res}'
        else :
            response_content = '出现非数学字符或计算式不成立，无法计算'
    else:
        response_content = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    to_user_name = xml.findtext('FromUserName')
    from_user_name = xml.findtext('ToUserName')
    create_time = str(int(time.time()))
    msg_type = 'text'

    response_xml = f"""
        <xml>
            <ToUserName><![CDATA[{to_user_name}]]></ToUserName>
            <FromUserName><![CDATA[{from_user_name}]]></FromUserName>
            <CreateTime>{create_time}</CreateTime>
            <MsgType><![CDATA[{msg_type}]]></MsgType>
            <Content><![CDATA[{response_content}]]></Content>
        </xml>
    """
    return response_xml


if __name__ == '__main__':
    app.run(debug=True)
