import os
import socket
import json
import time
import sys
key="3dggswfbwkd3nashv830189yf1ai1o5vkpc12xga0j1qyuik3gubh82wh1f47rmqq9e341dncj5voi0uuibh50wn7ft1wr2kbpzbm91v6mrxyh5w0usz43jbjhnefnr3utfy22k19ntltcn04ab19dozvu41lt58f1yb8m3512pp3ry7vhl2robcj2zpuuyv53031k9m6s7rpnxplgimxhobl605seaphrqt1cuui1xtotscjarphez2jwj8emt1nh09z7s7i085zs2p2x2l9i5xb4bqjxyzhtr46i9e96kdyl2zeb6ip1uhxia25yi1tcarp4wotu5kkjfdklv8zrv1mqimeph671sf4dbkjidqdqph0jh7jw6tl755netlz5lyodc1n5kvtbbjsyh0ufcl84p64taz054gvrlsxta2q8iv5tqbikptzk5pw7enxbpz9ckctrvl95wehgg9vlyfuhej5suvpl0we1xqaor32e8pxwl6kyg9vkjiglps"
# key='12345'

while True:
    overheat_protection_now=0#时间戳
    overheat_protection_threshold=5*60#强制关机阈值
    server=(input("ANDRESS:"),int(input("PORT:")))
    sock=socket.socket()
    try:
        sock.connect(server)
    except:
        print("[!] CONNECT FAILED")
        continue
    sock.send(key.encode())
    time.sleep(3)
    os.system('clear')
    while True:
        sock.send("get_temp".encode())
        p=sock.recv(1024)
        p=json.loads(p.decode().replace("\'","\""))
        str1='\r'
        for i in p.items():

            if 'cpu' in i[0] and i[1] >= 100 or 'gpu' in i[0] and i[1] >= 86:
                if overheat_protection_now==0:
                    overheat_protection_now=time.time()
                sock.send('overheat_warning'.encode())
                print("\033[0;31;40m!!!WARNING!!! OVERHEAT\033[0m\n"*100)
                time.sleep(12)
                os.system('clear')
            else:
                if 'cpu' in i[0] and i[1] < 99 or 'gpu' in i[0] and i[1] < 85:
                    overheat_protection_now=0

            if overheat_protection_now+overheat_protection_threshold<=time.time():
                sock.send('overheat_protection')
                print("\033[0;31;40m!!!WARNING!!! OVERHEAT PROTECTION ACTIVATED - YOUR COMPUTER ARE EXECUTING SHUTDOWN COMMAND\033[0m\n" * 100)
                input()




            if i[1] > 85:
                color = "\033[0;31;40m"
            elif i[1] > 75:
                color="\033[0;33;40m"
            else:
                color="\033[0m"

            str1+=f"{color}{i[0]}\t{i[1]}℃\033[0m  "

        sys.stdout.write(str1)
        sys.stdout.flush()

        time.sleep(0.5)

