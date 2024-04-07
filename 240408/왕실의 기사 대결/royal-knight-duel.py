import sys
from collections import deque
import copy


L,N,Q = map(int,sys.stdin.readline().split())

field =[]
knightfield = []
for _ in range(L):
    temp = list(map(int,sys.stdin.readline().split()))
    field.append(temp)
    knightfield.append([-1]*L)
knights = dict()
for i in range(N):
    yy,xx,hh,ww,kk = map(int,sys.stdin.readline().split())
    knights[i] = [yy-1, xx-1 ,hh, ww, kk]

    for y in range(knights[i][0], knights[i][0]+knights[i][2]):
        for x in range(knights[i][1], knights[i][1]+ knights[i][3]):
            knightfield[y][x] = i

order = []
for i in range(Q):
    kn, di = map(int,sys.stdin.readline().split())
    order.append((kn-1,di))

DIR = [(-1,0),(0,1),(1,0),(0,-1)]

# 0 -> 칸, 1-> 함정, 2-> 벽
# 0 -> y, 1 -> x, 2 -> 높이(y), 3 -> 너비(x), 4 -> 체력
# 체스판 밖도 벽이다..
# 이거도 마찬가지로 표와 dic 의 동기화가 매우 중요

# 백트래킹. 혹은 트랜잭션 원리 이용해야할거같은데...
# 이 메소드가 전부다. ret => 이동이 가능한가?, 이동했다면 처음 움직인것들을 제외한 나머지 움직인것들의 번호는?, 움직이고난 모양은? (t_field)
def movekight(ordd):
    blockqueue = deque()
    visited = [False] * N
    blockqueue.append(ordd[0])
    visited[ordd[0]] = True
    key = True
    moveblock = []
    dy,dx = DIR[ordd[1]]

    while blockqueue and key:
        wh = blockqueue.pop()
        for y in range(knights[wh][0]+dy, knights[wh][0]+knights[wh][2]+dy):
            for x in range(knights[wh][1]+dx, knights[wh][1]+ knights[wh][3]+dx):
                if field[y][x] == 2 or y < 0 or y >= L or x < 0 or x >= L:
                    key = False
                    break

                # 움직이면서 만난 번호들 저장.
                if t_knfield[y][x] != -1 and t_knfield[y][x] != wh and not visited[t_knfield[y][x]]:
                    blockqueue.appendleft(t_knfield[y][x])
                    moveblock.append(t_knfield[y][x])
                    visited[t_knfield[y][x]] = True
                
                # 블럭 이동시키기
                t_knfield[y][x] = wh


    if key:
        return True, moveblock

    else:
        return False, []

def damage(what):
    tmp = 0
    # 각각의 블럭에 함정이 몇개일까?
    for i in what:
        for y in range(knights[i][0], knights[i][0]+knights[i][2]):
            for x in range(knights[i][1], knights[i][1]+ knights[i][3]):
                if field[y][x] == 1:
                    tmp += 1
                    knights[i][4] -= 1
                    if knights[i][4] == 0:
                        knights.pop(i)
    return tmp

# 딕셔너리 동기화
def movekn(wh, d):
    dy,dx = DIR[d]
    for i in wh:
        knights[i][0] += dy
        knights[i][1] += dx


ans = 0
for i in range(Q):
    t_knfield = copy.deepcopy(knightfield)
    # 움직임이 가능한지, 만약 가능하다면 어떻게 움직이는지
    is_move, what = movekight(order[i])
    # 이미 움직임은 확정이 나있으니까 어떤것들이 움직인건가 확인만 하자.
    if is_move:
        knightfield = t_knfield
        movekn(what, order[i][1])
        ans += damage(what)

print(ans)