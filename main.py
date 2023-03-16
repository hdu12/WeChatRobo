from wxauto import *
import threading
import sqlite3
import emoji
import schedule
import time
import datetime

# 获取当前微信客户端
wx = WeChat()
#定义聊天对象
who = '文件传输助手'
# 获取会话列表
wx.GetSessionList()

emoji = emoji.emojize(":gift_heart:",language='alias') + "05机器人" + emoji.emojize(":gift_heart:",language='alias')
def hello():
    #获取当前消息
    msgs = wx.GetAllMessage
#for msg in msgs:
#    print('%s : %s'%(msg[0], msg[1]))
    sendAll=""
#最新的一条消息
    msg = msgs[-1]
#只获取消息内容
    msg=msg[1]
#连接数据库
    conn = sqlite3.connect('测试.db')
    cursor = conn.cursor()

#进行判断
    if msg.find(" mark") != -1:   
       msg=msg.split(" mark") 
       if msg[0].find("@") != -1:      
          msg=msg[0].split("@")
          print(msg[0] + msg[1])
          sendAll="\n" + "已注册："+ msg[1] + "  日期：" + msg[0]
          conn.execute("INSERT INTO mark(text, date) VALUES ('%s', '%s')"%(msg[1],msg[0]))
          


       else: 
             sendAll="\n" + "已注册："+ msg[0]
             conn.execute("INSERT INTO mark (text) values ('%s')"%(msg[1]))

             
    elif msg == "Mark":
         db=conn.execute("SELECT id, text, date from mark")  
         
         for row in db:
            date = row[2]
            if type(date) is str:
               sendMsg=str(row[0]) + "." + str(row[1]) + "---" + str(row[2])
               sendAll = sendAll +"\n" + sendMsg
               print(sendAll)
            else:      
               sendMsg=str(row[0]) + "." + str(row[1])
               sendAll = sendAll +"\n" + sendMsg
               if len(sendAll) == 0:
                  sendAll = emoji +"/n无数据"
                  
    elif msg.find("Delete ") != -1:
         msg=msg.split(" ")
         cursor.execute("DELETE from mark where id=%s;"%(msg[1]))  
         conn.commit()
         sendAll = "\n已删除序号：" + msg[1]

    elif msg == "DeleteAll":
         cursor.execute("DELETE from mark;")  
         conn.commit()
         sendAll = "\n已清空数据"

    if len(sendAll) != 0:
       sendAll = emoji + sendAll
       WxUtils.SetClipboard(sendAll)    # 将内容复制到剪贴板，类似于Ctrl + C
       wx.ChatWith(who)                 # 打开`文件传输助手`聊天窗口
       wx.SendClipboard()   
       conn.close()

def hello2():
    conn = sqlite3.connect('测试.db')
    cursor = conn.cursor()
    db=conn.execute("SELECT id, text, date from mark")  
    today = datetime.date.today()
    dailysend = emoji + "\n" + "今日提醒日程："
    for row in db:
        if type(row[2]) is str:
            date=row[2].split("/")
            month = date[0]
            day = date[1]
            if str(today.month) == month and str(today.day) == day:
                sendmsg = str(row[0]) + "." + str(row[1])
                dailysend = dailysend +"\n"+ sendmsg            
               
    WxUtils.SetClipboard(dailysend)    # 将内容复制到剪贴板，类似于Ctrl + C
    wx.ChatWith(who)                 # 打开`文件传输助手`聊天窗口
    wx.SendClipboard()  
    conn.close()        

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(3).seconds.do(run_threaded, hello)
schedule.every().day.at("08:30").do(run_threaded,hello2)
while True:
    schedule.run_pending()
    time.sleep(1)

