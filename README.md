# cdutetc_class_push
处理成理工程（成都理工大学工程技术学院）官方网站的json课表，并且通过微信公众号推送课程信息

边学边写的，代码较乱，请见谅


代码仅供学习交流使用，如果您认为该仓库的任何代码侵犯了您的利益，请及时联系我：abuse@6688669.xyz


如果有任何想法或需要帮助，欢迎联系：chat@6688669.xyz


使用方法：
1.拉取代码，抓包获取学校的课表json文件放到相同目录
2.sudo su（可选操作）
3.screen -S wxpush #建立一个叫wxpush的screen，方便后续维护，wxpush可以随意替换你想要的名字
4.python3 pusher.py
恢复screen：
screen -r wxpush
以下为实现功能演示：
/next 功能

![image](https://github.com/guesserx/cdutetc_class_push/blob/main/2024-04-25_235554.png)

/today_now和/now，/next_class和前者功能相似，此处不演示

![image](https://github.com/guesserx/cdutetc_class_push/blob/main/2024-04-25_235941.png)

/send和/receive 收发消息

![image](https://github.com/guesserx/cdutetc_class_push/blob/main/2024-04-26_000219.png)
