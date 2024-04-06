import sys

n,m,p,c,d = map(int,sys.stdin.readline().split())

SDIR = [(-1,0),(0,1),(1,0),(0,-1)]
RDIR = [(-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1),(0,1),(0,-1)]

# field, rou, santa 따로따로 관리하자.
field = [[-1]*n for _ in range(n)]

ry,rx = map(int,sys.stdin.readline().split())
ry -= 1
rx -= 1
field[ry][rx] = -2

santa = dict()
for i in range(p):
    num,sy,sx = map(int,sys.stdin.readline().split())
    # 맨뒤는 기절깰때까지 남은 턴수
    santa[num-1] = [sy-1,sx-1,0]
    field[sy-1][sx-1] = num-1


def roumove():
    global ry,rx
    # 가장 가까운 산타를 향해
    mm = (float('inf'),float('inf'),float('inf'),0) # n만큼, y, x,몇번

    for i in santa.keys():
        dis = (santa[i][0] - ry) ** 2 + (santa[i][1] - rx) ** 2
        tempm = (dis, -santa[i][0], -santa[i][1],i)
        mm = min(tempm,mm)

    # 루돌프 떠남
    field[ry][rx] = -1
    ddd = [0,0]
    coll = False
    if ry > -mm[1]:
        if ry > 0:
            ry -= 1
            ddd[0] -= 1
    elif ry < -mm[1]:
        if ry < n-1:
            ry += 1
            ddd[0] += 1
    
    if rx > -mm[2]:
        if rx > 0:
            rx -= 1
            ddd[1] -= 1
    elif rx < -mm[2]:
        if rx < n-1:
            rx += 1
            ddd[1] += 1

    # 루돌프 다시 도착, 거기 산타가 있을때
    if field[ry][rx] >= 0:
        coll = field[ry][rx]
        field[ry][rx] = -2
        # 점수 주기
        score[mm[3]] += c
        # 기절시키기
        santa[mm[3]][2] = 2

        return ddd,coll
    
    else:
        field[ry][rx] = -2
        return -1, -1
    
    
    
def roucollision(dd,nn,cc):
    rmy,rmx = dd
    # dd 방향대로 산타를 밀어낸다.
    santa[nn][0] += rmy*cc
    santa[nn][1] += rmx*cc
    # 맞다.
    if 0 <= santa[nn][0] < n and 0 <= santa[nn][1] < n:
        # 도착한곳에 이미 있다면?
        if field[santa[nn][0]][santa[nn][1]] != -1:
            befrou = field[santa[nn][0]][santa[nn][1]]
            field[santa[nn][0]][santa[nn][1]] = nn
            roucollision(dd,befrou,1)
        else:
            field[santa[nn][0]][santa[nn][1]] = nn
    # 아니다.
    else:
        santa.pop(nn)


def sanmove(s):
    global ry,rx, d
    # s번 산타의 무빙
    sy, sx ,die = santa[s][0], santa[s][1], santa[s][2]

    if die > 0:
        santa[s][2] -= 1
        return -1, False

    mindis = (float('inf'),float('inf')) # 거리, 방향.
    for i in range(4):
        dy,dx = SDIR[i]
        if 0<= sy+dy < n and 0<= sx+dx < n and field[sy+dy][sx+dx] < 0: # 산타가 있는 곳으로는 x
            if (((sy + dy) - ry) ** 2 + ((sx + dx) - rx) ** 2) < ((sy - ry) ** 2 + (sx - rx) ** 2):
                ddd = (((sy + dy) - ry) ** 2 + ((sx + dx) - rx) ** 2, i)
                mindis = min(mindis, ddd)
    
    # mindis 의 [1] 이 산타의 이동 방향. 저거의 반대가 맞다.
    reald = (mindis[1]+2) % 4

    # 산타 안움직
    if mindis[1] == float('inf'):
        return -1, False


    dy,dx = SDIR[mindis[1]]
    santa[s][0] += dy
    santa[s][1] += dx

    if mindis[0] > 0:
        field[sy][sx] = -1
        field[sy+dy][sx+dx] = s
        return -1, False
    else:
        field[sy][sx] = -1
        score[s] += d
        santa[s][2] = 1
        return reald, True  


def sancollision(dd,nn,cc):
    ddy,ddx = SDIR[dd]
    # d 방향대로 산타를 밀어낸다.
    santa[nn][0] += ddy*cc
    santa[nn][1] += ddx*cc
    # 맞다.
    if 0 <= santa[nn][0] < n and 0 <= santa[nn][1] < n:
        # 도착한곳에 이미 있다면?
        if field[santa[nn][0]][santa[nn][1]] != -1:
            befsan = field[santa[nn][0]][santa[nn][1]]
            field[santa[nn][0]][santa[nn][1]] = nn
            sancollision(dd,befsan,1)
        else:
            field[santa[nn][0]][santa[nn][1]] = nn
    # 아니다.
    else:
        santa.pop(nn)


score = [0] * p
for _ in range(m):

    if santa:
        # 루돌프 움직임
        dd, coll = roumove()
        
        if coll >= 0:
            # 루돌프 충돌
            roucollision(dd,coll,c)
    else:
        break
    if santa:
        # 산타 움직임
        for i in range(p):
            tttt = santa.keys()
            if i in tttt:
                dd, col = sanmove(i)
                if col:
                    # 산타 충돌
                    sancollision(dd, i, d)
    else:
        break
    # 남은 산타 점수 추가.
    for i in santa.keys():
        score[i] += 1

print(*score)