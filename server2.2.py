# -*- coding:utf-8 -*-
from socket import *
from threading import *
import sys 
from time import sleep
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',6666))
s.listen(4)
# 存储用户名和 套接字 文件描述符 s.fileno() 的列表
#存储每一个套接字的列表
#遍历 套接字 列表 如果 该套接字的文件描述符 和 自身不同 则为另一个套接字对象
# 需要被提供  
# user_list[user1,user2]
# 包括user_id 以及 该用户连接服务器的套接字  user1  user_id1:c1   user2  user_id2:c2
l = []
ready=0
def clientrecv(mysock,myfile):
    global ready

    l.append(mysock)
    
    # mysock.send('chushihua'.encode())
    while 1:


        myinfo = mysock.recv(4096)
        # myinfo+=myinfo

        # if myinfo.decode()[0] == '' 
        myinfo=myinfo.decode()
        if myinfo:
            print(myinfo)
            if myinfo=='zhunbei':
                ready+=1
            if myinfo== 'quxiao':
                ready-=1
            if myinfo!='judgefirst'and myinfo!='first' and myinfo!='zhunbei' and myinfo!='quxiao' and myinfo!='' and myinfo!='second':
                for c in l:
                    if c.fileno() != myfile:
                        
                        c.send(myinfo.encode())
            # if myinfo=='win1' or 'win2':
            #     l=[]
            print(ready)

def serversend(c):
    #当服务器接收到两个客户端准备消息后，发送 judgefirst
    global ready
    if c==l[0]:
        flag = 0
        while 1:
            if ready==2 and flag == 0:
                sleep(1)
                l[1].send('judgefirst'.encode())
                l[0].send('judgefirst'.encode())
                flag = 1
                continue


                

            if flag ==1:
                sleep(1)
                l[1].send('first'.encode())
                l[0].send('second'.encode())
                ready = 0 
                flag = 0
            


while 1:

    try :
        c,addr = s.accept()
        print('connect from ',addr,c.fileno())

    except KeyboardInterrupt:
        c.close()
        sys.exit('服务器退出')
    except Exception as e:
        print(e)
        continue
    finally:
        print('一次连接')
    #主线程接收信息，
    # info = c.recv(1024).decode()
    # info.split(',')
    #对信息 进行解析 分类处理  [userid,type,ifformation]
    # if info

    t1 = Thread(target = clientrecv,args=(c,c.fileno()))
    t2 = Thread(target = serversend,args=(c,))
    # t2 = Thread(target = clientsend,args=(c,c.fileno()))
    t1.setDaemon(True)
    t1.start()
    t2.setDaemon(True)
    t2.start()
    # t2.setDaemon(True)
    # t2.start()

# 服务器端 每个 用户接入 创建新的进程/线程 同时在线多人，

# 套接字 文件描述符 用户名

# 注册 登录  登录后 将用户名 和对应的套接字 存于字典
# 所有套接字 存于列表 以用户名为 键 建立连接的 套接字为 值 创建字典 {username:(mysock,mysock.fileno())}
# 套接字对象 类
# class sockobj:
#     def __init__(self,):


# 数据库 mysql 

# id username password  信息足够


# 在线的  连接中的列表  断开 即删除
# 服务器端储存用户的用户列表 随机匹配出两个 进行对战游戏
