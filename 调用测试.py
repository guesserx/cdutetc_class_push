import saerch_self
import classls

#测试当前课程相关代码
name,room,class_time,class_time_n= saerch_self.fun(0)
response_content = f'课程：{name}\n教室：{room}\n节数：{class_time}\n上课时间 ：{class_time_n}'
print(response_content)
print(saerch_self.fun(0))
#测试异常处理
print(saerch_self.fun(999))
#测试输出今日所有课程是否有问题
names, rooms, class_times, class_time_ns = saerch_self.fun(1)
final_content = ''
i = 0
if '今日无课' not in str(names) :
    for name in names:
        final_content += f'课程：{name}\n教室：{rooms[i]}\n节数：{class_times[i]}\n上课时间 ：{class_time_ns[i]}'
        i += 1
    response_content = final_content
    print(response_content)
else :
    response_content ='🎉今日无课'
    print(response_content)
#测试输出以后几天课程的代码
days_add = 1
names, rooms, class_times, class_time_ns = saerch_self.next_days(days_add)
final_content = ''
i = 0
if '无课' not in str(names):
    for name in names:
        final_content += f'📖课程：{name}\n⛪︎教室：{rooms[i]}\n节数：{class_times[i]}\n上课时间 ：{class_time_ns[i]}\n====\n'
        i += 1
    response_content = final_content
    print(response_content)
else:
    response_content = f'{days_add}日后无课'
    print(response_content)
#最近的课程代码
print(saerch_self.today_next_class())
#更新课表
print(classls.get_new())