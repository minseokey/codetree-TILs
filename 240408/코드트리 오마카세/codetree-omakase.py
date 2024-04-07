import sys
from collections import deque

L,Q = map(int,sys.stdin.readline().split())

table = deque([dict() for _ in range(L)])
wait = [dict() for _ in range(L)]
waitlis = set()
waitpeo = []
sushi = 0
start = 0

def make(tlis):
    global sushi
    sushi += 1
    x,name = int(tlis[0]) ,tlis[1]
    if name in table[x].keys():
        table[x][name] += 1
    else:
        table[x][name] = 1


def enter(tlis):
    x,name,n = int(tlis[0]),tlis[1],int(tlis[2])
    wait[x][name] = n
    waitlis.add(name)
    waitpeo.append(x)


def photo():
    print(len(waitlis),sushi)
    
def rotate():
    temp = table.pop()
    table.appendleft(temp)

def eat():
    global sushi
    for i in waitpeo:
        # 대기중인 이름들
        for n in wait[i].keys():
            if n in table[i].keys():
                wait[i][n] -= table[i][n]
                sushi -= table[i][n]
                table[i].pop(n)
                if wait[i][n] == 0:
                    waitlis.remove(n)   


for i in range(Q):
    temp = sys.stdin.readline().split()
    for i in range(int(temp[1])-start):
        rotate()
        eat()

    start = int(temp[1])

    if temp[0] == "100":
        make(temp[2:])
        eat()
    elif temp[0] == "200":
        enter(temp[2:])
        eat()
    else:
        eat()
        photo()