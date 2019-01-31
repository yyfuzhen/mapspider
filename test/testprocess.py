# -*- coding:utf-8 -*-
import math
import threading
import time

__author__ = 'zhennehz'

def music(func):
    for i in range(3):
        print("I was listening to %s. %s" %(func,time.ctime()))
        time.sleep(1)

def movie(func):
    for i in range(3):
        print("I was at the %s! %s" %(func, time.ctime()))
        time.sleep(3)

def super_player(name,ss):
    for i in range(2):
        print("Start playing： %s! %s" %(name, time.ctime()))
        time.sleep(ss)

'''
threads = []
t1 = threading.Thread(target=music,args=('爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=movie,args=('阿凡达',))
threads.append(t2)

'''
#播放的文件与播放时长
list = {'爱情买卖.mp3':3,'阿凡达.mp4':5,'我和你.mp3':4}

threads = []
files = range(len(list))

#创建线程
for name in list.items():
    t = threading.Thread(target=super_player,args=(name[0],name[1]))
    threads.append(t)


if __name__ == '__main__':

    #for t in threads:
    #    t.setDaemon(True)
    #    t.start()

    #t.join()


    # 启动线程
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()

    #print("all over %s",time.ctime())


    '''
    tot = 6299
    count = 100
    step = math.ceil(tot/count)
    print("step="+str(step))
    arr1 = []
    arr2 = []
    for i in range(count):
        print("index:"+str(i+1)+ " from:"+str(i*step+1)+" to:"+str((i+1)*step))
        arr1.append(i*step+1)
        arr2.append((i+1)*step)

    for i in range(len(arr1)):
        print(str(arr1[i])+"--"+str(arr2[i]))
    '''
