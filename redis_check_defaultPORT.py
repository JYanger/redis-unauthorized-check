# _*_  coding:utf-8 _*_
#! /usr/bin/env python
# changed by Jyanger 
import socket
import random
import sys
import threading,Queue,time

PASSWORD_DIC=['redis','root','oracle','password','p@aaw0rd','abc123!','123456','admin','12345678','666666','88888888','1234567890','888888']
socket.setdefaulttimeout(1)            #socket超时设置
ports = ['6379','6380','6377','6389','6369']

class MyThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:  # 除非确认队列中已经无任务，否则时刻保持线程在运行
            try:
                ip = self.queue.get(block=False)   # 如果队列空了，直接结束线程。根据具体场景不同可能不合理，可以修改
                check(ip,)
            except Exception as e:
                break    

def check(ip):
    for port in ports:
        try:
            socket.setdefaulttimeout(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.send("INFO\r\n")
            result = s.recv(1024)
            if "redis_version" in result:
                time.sleep(random.random())
                print "[+]                 {}                 {}                   unauthorized                 ".format(ip,port)
                
            elif "Authentication" in result:
                for pass_ in PASSWORD_DIC:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, int(port)))
                    s.send("AUTH %s\r\n" %(pass_))
                    result = s.recv(1024)
                    if '+OK' in result:
                        time.sleep(random.random())
                        print "[+]                 {}                {}              week_password: {} ".format(ip,port,pass_)

                
        except Exception as e:
            pass
    
def run(ipaddress,Thread_count):                     #此处设置线程数
    threads = []
    number = 0
    queue = Queue.Queue()
    file = open(ipaddress,'r')
    for url in file.readlines():
        url=url.replace('\n','')
        queue.put(url)
        number = number+1                     #统计url总数
    file.close()
    for i in range(Thread_count):
        threads.append(MyThread(queue))
    #print u"[+]------------------------------------total ip "+ str(number)+u"------------------------------------------"
    for t in threads:
        try:
            t.start()
        except Exception as e:
            print e
            continue
    for t in threads:
        try:
            t.join()
        except Exception as e:
            print e
            continue
if __name__ == '__main__':
    
    if len(sys.argv)!=3:
        print u"usage: pyhton redis_check_defaultPORT.py ip.txt(扫描地址)  threads(线程)"
    else:
        print "[*]------------------------------------------------------------------------------------------------"
        print "[*]-----------------------start redis  unauthorized check start------------------------------------"
        print "[*]---------------|   ipaddress   |-----------|  port  |--------------|  type/pass  |--------------"
        run(sys.argv[1],int(sys.argv[2]))
        print "[*]cherk all ip end, goodbey!"
