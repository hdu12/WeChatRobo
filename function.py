import sqlite3
import datetime

def mark(conn, msg):
    cursor = conn.cursor()
    msg = msg.split(" mark") 
    if msg[0].find("@") != -1:      
        msg = msg[0].split("@")
        print(msg[0] + msg[1])
        sendAll = "\n已注册：" + msg[1] + "  日期：" + msg[0]
        cursor.execute("INSERT INTO mark(text, date) VALUES (?, ?)", (msg[1], msg[0]))
    else: 
        sendAll = "\n已注册：" + msg[0]
        cursor.execute("INSERT INTO mark (text) values (?)", (msg[0],))
    conn.commit()
    return sendAll

def Mark(conn,msg):
    #设置发送消息为空字符串
    sendAll=""
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, date from mark")   
    db = cursor.fetchall()
    if len(db) > 0:
        for row in db:
            date = row[2]            
            if type(date) is str:
               sendMsg=str(row[0]) + "." + str(row[1]) + "---" + str(row[2])
               sendAll = sendAll +"\n" + sendMsg
               print(sendAll)

            else:      
                sendMsg=str(row[0]) + "." + str(row[1]) 
                sendAll = sendAll +"\n" + sendMsg             
           
               
    else: 
        sendAll = "\n无数据"  
    return sendAll

def delete(conn,msg):
    cursor = conn.cursor()
    msg=msg.split(" ")
    cursor.execute("DELETE from mark where id=?;",(msg[1]))  
    conn.commit()
    sendAll = "\n已删除序号：" + msg[1]
    return sendAll
    
def deleteall(conn,msg):
    cursor = conn.cursor()
    cursor.execute("DELETE from mark;")  
    conn.commit()
    sendAll = "\n已清空数据"
    return sendAll

def note(conn):    
    cursor = conn.cursor()
    cursor.execute("SELECT id, text, date from mark") 
    db = cursor.fetchall() 
    today = datetime.date.today()
    dailysend = "\n" + "今日提醒日程："
    print(dailysend)
    for row in db:
        print(row[1])
        if type(row[2]) is str:
            date=row[2].split("/")
            month = date[0]
            day = date[1]
            if str(today.month) == month and str(today.day) == day:
                sendmsg = str(row[0]) + "." + str(row[1])
                dailysend = dailysend +"\n"+ sendmsg
    if dailysend == "\n" + "今日提醒日程：":
       return dailysend + "无"
    else: 
        return dailysend