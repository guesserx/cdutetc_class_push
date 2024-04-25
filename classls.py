import json
import os
import requests

url = 'http://jwgl.cdutetc.cn:801/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=Nxxxx'#这里修改成抓包到正常的url，即gnmkdm=N后面是数字
headers = {
#这里填ua
}
data = '这里填data'




def get_new() :
    try :
        #proxy_pool = {'http': 'http://user:pwd@ip:port'}
        #response = requests.post(url, headers=headers, data=data, proxies=proxy_pool)
        '''如果是海外服务器就取消注释上诉代码，学校网站禁止了海外ip访问
            注意：请自行修改代理服务器相关配置，默认是http，相关用法已经标注
        '''
        response = requests.post(url, headers=headers, data=data)
        if 'qsxqj' in response.text:
            try :
                class_data = json.loads(response.text)
                if class_data['sjkList'][0]['dateDigit'] != None :
                    if os.path.exists('old_list.json') :
                        os.remove('old_list.json')
                    os.rename('kblist.json', 'old_list.json')
                    newcs = open('kblist.json', 'w', encoding='utf-8')
                    newcs.write(response.text)
                    return '更新成功！时间：'+class_data['sjkList'][0]['dateDigit']
            except Exception as e:
                    return '在处理字典时发生错误：' + str(e)
        else :
            return '更新失败，可能是身份信息已过期'
    except Exception as e:
        return '在尝试与学校服务器连接时发生错误：'+str(e)
