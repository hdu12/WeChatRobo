from wxauto import *
from weather_ref import *
from function import *
import threading
import sqlite3
import emoji
import schedule
import time



# 获取当前微信客户端
wx = WeChat()
#定义聊天对象
who = '欢喜小猪૮₍ ˃ ⤙ ˂ ₎ა  ๑ᵒ'
# 获取会话列表
wx.GetSessionList()
#使用Emoji对于标题美化
emoji = emoji.emojize(":gift_heart:",language='alias') + "05机器人" + emoji.emojize(":gift_heart:",language='alias')

#读取最新消息以及反馈主函数
def hello():
#获取当前消息
    msgs = wx.GetAllMessage
 #设置发送消息为空字符串
    sendAll=""
#读取最新的一条消息
    msg = msgs[-1]
#只获取消息内容本身
    msg=msg[1]
#进行判断
    if msg.find(" mark") != -1:   
       with sqlite3.connect('测试.db') as conn:
           sendAll = mark(conn, msg)
             
    elif msg == "Mark":
       with sqlite3.connect('测试.db') as conn:
           sendAll = Mark(conn, msg)
            
    elif msg.find("Delete ") != -1:
       with sqlite3.connect('测试.db') as conn:
           sendAll = delete(conn, msg)       

    elif msg == "DeleteAll":
       with sqlite3.connect('测试.db') as conn:
           sendAll = deleteall(conn, msg)

    elif msg =="weather":
        sendAll = weather_real()

    elif msg =="weatherr":
        sendAll = weather_ref()       

    if len(sendAll)!=0:
      sendAll = emoji + sendAll
      WxUtils.SetClipboard(sendAll)    # 将内容复制到剪贴板，类似于Ctrl + C
      wx.ChatWith(who)                 # 打开`文件传输助手`聊天窗口
      wx.SendClipboard()   
      #conn.close()

def hello2():
        with sqlite3.connect('测试.db') as conn: 
           dailysend = emoji + note(conn)
           WxUtils.SetClipboard(dailysend)    # 将内容复制到剪贴板，类似于Ctrl + C
           wx.ChatWith(who)                 # 打开`文件传输助手`聊天窗口
           wx.SendClipboard()         

#线程启动
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

#定时循环
schedule.every(5).seconds.do(run_threaded, hello)
schedule.every().day.at("08:30").do(run_threaded,hello2)
schedule.every().day.at("08:25").do(run_threaded,weather_ref)
#schedule.every(20).seconds.do(run_threaded,hello2)
while True:
    schedule.run_pending()
    time.sleep(1)