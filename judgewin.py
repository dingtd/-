l = [[0 for i in range(15)] for i in range(15)]
i = 0
while 1:
    if i%2 == 0:
        [x,y] = input()
        l[x][y] = 1
    else:
        l[x][y] = 2
    if l[x][y]
def first():
    #　１　黑　２　白

def black():

def white():

def judge():
    #判断黑棋
    if l[x][y] = 1:
        #横　　左计数＋右计数　＝＝5　　x　i  y不变
        count = 1
        count1 = 0
        count2 = 0
        x = i
            while 1:
                i -= 1
                if l[i][y] == 1:
                    count1 += 1
                else:
                    break
            while 1:
                x += 1
                if l[x][y] == 1:
                    count2 += 1
                else:
                    break


        #竖  x不变　　　y i
        #左斜 x-1 y-1 x+1 y+1
        #右斜 x-1 y+1 x+1 y-1
    #判断白棋
    if l[x][y] = 2:




def wuzi():

def row():
    count = 1
            count1 = 0
            count2 = 0
            x = i
                while 1:
                    i -= 1
                    if l[i][y] == 1:
                        count1 += 1
                    else:
                        break
                while 1:
                    x += 1
                    if l[x][y] == 1:
                        count2 += 1
                    else:
                        break
            if count+count1+count2 == 5:
                def win()
            else:
                def shu()
def shu():
    count = 1
            count1 = 0
            count2 = 0
            y = i
                while 1:
                    i -= 1
                    if l[x][i] == 1:
                        count1 += 1
                    else:
                        break
                while 1:
                    y += 1
                    if l[x][y] == 1:
                        count2 += 1
                    else:
                        break
            if count+count1+count2 == 5:
                def win()
            else:
                def lift()
def lift():
    #左斜 x-1 y-1 x+1 y+1
        count = 1
            count1 = 0
            count2 = 0
            x = i
            y = j
                while 1:
                    i -= 1
                    j -=1

                    if l[i][j] == 1:
                        count1 += 1
                    else:
                        break
                while 1:
                    x += 1
                    y += 1
                    if l[i][y] == 1:
                        count2 += 1
                    else:
                        break
            if count+count1+count2 == 5:
                def win()
            else:
                def right()
def right():
    #右斜 x-1 y+1 x+1 y-1
        count = 1
        count1 = 0
        count2 = 0
        x = i
        y = j
            while 1:
                i -= 1
                j += 1
                if l[i][j] == 1:
                    count1 += 1
                else:
                    break
            while 1:
                x += 1
                if l[x][y] == 1:
                    count2 += 1
                else:
                    break
        if count+count1+count2 == 5:
            def win()
        else:
            def xiaqi()
def xiaqi():