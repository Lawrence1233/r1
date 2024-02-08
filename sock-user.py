import os
import socket
import json
import time
import sys
import re
import traceback

key="3dggswfbwkd3nashv830189yf1ai1o5vkpc12xga0j1qyuik3gubh82wh1f47rmqq9e341dncj5voi0uuibh50wn7ft1wr2kbpzbm91v6mrxyh5w0usz43jbjhnefnr3utfy22k19ntltcn04ab19dozvu41lt58f1yb8m3512pp3ry7vhl2robcj2zpuuyv53031k9m6s7rpnxplgimxhobl605seaphrqt1cuui1xtotscjarphez2jwj8emt1nh09z7s7i085zs2p2x2l9i5xb4bqjxyzhtr46i9e96kdyl2zeb6ip1uhxia25yi1tcarp4wotu5kkjfdklv8zrv1mqimeph671sf4dbkjidqdqph0jh7jw6tl755netlz5lyodc1n5kvtbbjsyh0ufcl84p64taz054gvrlsxta2q8iv5tqbikptzk5pw7enxbpz9ckctrvl95wehgg9vlyfuhej5suvpl0we1xqaor32e8pxwl6kyg9vkjiglps"
# key='12345'
memory=[]
email_key="raspberry"

def send_email(p:socket.socket,receiver:str,text:str):
    """
    :param p: socket variable
    :return:
    """

    p.send("send_email".encode())
    message=p.recv(1024)
    if "CONTINUE" not in message.decode():
        return 0

    p.send(str((receiver,text)).encode())
    message = p.recv(1024)
    if "CONTINUE" not in message.decode():
        return 0

print("""
  ____       _      ____    ____    ____    _____   ____    ____   __   __      
 |  _ \     / \    / ___|  |  _ \  | __ )  | ____| |  _ \  |  _ \  \ \ / /      
 | |_) |   / _ \   \___ \  | |_) | |  _ \  |  _|   | |_) | | |_) |  \ V /       
 |  _ <   / ___ \   ___) | |  __/  | |_) | | |___  |  _ <  |  _ <    | |        
 |_| \_\ /_/   \_\ |____/  |_|     |____/  |_____| |_| \_\ |_| \_\   |_|        
                                                                                
   ____                                       _                                 
  / ___|   ___    _ __ ___    _ __    _   _  | |_    ___   _ __                 
 | |      / _ \  | '_ ` _ \  | '_ \  | | | | | __|  / _ \ | '__|                
 | |___  | (_) | | | | | | | | |_) | | |_| | | |_  |  __/ | |                   
  \____|  \___/  |_| |_| |_| | .__/   \__,_|  \__|  \___| |_|                   
                             |_|                                                
  _   _                                _                                        
 | | | |   ___    _   _   ___    ___  | | __   ___    ___   _ __     ___   _ __ 
 | |_| |  / _ \  | | | | / __|  / _ \ | |/ /  / _ \  / _ \ | '_ \   / _ \ | '__|
 |  _  | | (_) | | |_| | \__ \ |  __/ |   <  |  __/ |  __/ | |_) | |  __/ | |   
 |_| |_|  \___/   \__,_| |___/  \___| |_|\_\  \___|  \___| | .__/   \___| |_|   
                                                           |_|                  
""")

time.sleep(3)
if os.system('clear'):  # 适配win/linux
    os.system('cls')
while True:
    overheat_protection_now=float('inf')#时间戳
    overheat_protection_threshold=5*60#强制关机阈值
    last_get_email=0#最后一次获取邮件
    get_email_delay=10#延迟10秒
    server=(input("ANDRESS:"),int(input("PORT:")))
    report="1424393706@qq.com"#汇报邮箱
    sock=socket.socket()
    try:
        sock.connect(server)
    except:
        print("[!] CONNECT FAILED")
        continue
    sock.send(key.encode())
    time.sleep(3)
    if os.system('clear'):#适配win/linux
        os.system('cls')
    while True:
        try:
            if get_email_delay+last_get_email<time.time():
                last_get_email=time.time()
                sock.send("read_email".encode())
                email_data=sock.recv(8192)
                email_data=json.loads(email_data.decode().replace("\'","\""))
                #->dict
                if email_data['Time']+60*3>time.time() and email_data["Hash"] not in memory:#丢弃超过3分钟/已处理的邮件
                    memory.append(email_data['Hash'])  # 丢弃
                    body = eval(re.compile(r"(\([^\(\)]*\))").findall(email_data["MailBody"])[0].replace(",","\",\"").replace("(","(\"").replace(")","\")"))  # safety
                    #->tuple
                    #(key,command,args)
                    if type(body) != tuple:
                        print("\033[0;31;40m[!] Incorrect command format,this email will be discarded.\033[0m\n")
                        raise TypeError

                    if body[0] != email_key:
                        print("\033[0;31;40m[!] Incorrect password\033[0m\n")
                        raise KeyError

                    match body[1]:
                        case "shutdown-s":
                            send_email(sock,email_data['MailSender'],"The RaspberryPi was accept the shutdown command,the computer will shutdown after 30 second. System command:shutdown -s -t 30")
                            sock.send("shutdown-s".encode())
                        case "shutdown-h":
                            send_email(sock,email_data['MailSender'], "The RaspberryPi was accept the hibernate command,the computer will shutdown immediately.System command:shutdown -h")
                            sock.send("shutdown-h".encode())
                        case "temp":
                            send_email(sock, email_data['MailSender'], str(p))
                        case "lockup":
                            send_email(sock, email_data['MailSender'],"Complete.Your computer is locked.")
                            sock.send("lockup".encode())
                        case _:
                            send_email(sock,email_data['MailSender'], "Error:Unknow command,please check the command then try again.")
        except:
            pass

        sock.send("get_temp".encode())
        p=sock.recv(1024)
        p=json.loads(p.decode().replace("\'","\""))
        str1='\r'
        for i in p.items():

            if 'cpu' in i[0] and i[1] >= 100 or 'gpu' in i[0] and i[1] >= 86:
                if overheat_protection_now==float('inf'):
                    overheat_protection_now=time.time()
                send_email(sock, report, f"Warning:Your computer has been continuously overheating for {time.time()-overheat_protection_now} seconds.Forced shutdown will be executed after {overheat_protection_now+overheat_protection_threshold-time.time()} seconds.")
                sock.send('overheat_warning'.encode())
                print("\033[0;31;40m!!!WARNING!!! OVERHEAT\033[0m\n"*100)
                time.sleep(12)
                if os.system('clear'):  # 适配win/linux
                    os.system('cls')
            else:
                if 'cpu' in i[0] and i[1] < 99 or 'gpu' in i[0] and i[1] < 85:
                    overheat_protection_now=float('inf')

            if overheat_protection_now+overheat_protection_threshold<=time.time():
                send_email(sock, report, f"Warning:Overheat protection activated,your computer will shutdown immediately,more information:{p}.")
                sock.send('overheat_protect'.encode())
                print("\033[0;31;40m!!!WARNING!!! OVERHEAT PROTECTION ACTIVATED - YOUR COMPUTER ARE EXECUTING SHUTDOWN COMMAND\033[0m\n" * 100)
                input()




            if i[1] > 85:
                color = "\033[0;31;40m"
            elif i[1] > 75:
                color="\033[0;33;40m"
            else:
                color="\033[0m"

            str1+=f"{color}{i[0]}\t{i[1]}'C\033[0m  "

        sys.stdout.write(str1)
        sys.stdout.flush()

        time.sleep(0.5)

