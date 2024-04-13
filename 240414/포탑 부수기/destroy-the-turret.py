import sys
from collections import deque
import copy
# 부서지지 않은 포탑 1 ? -> 게임 종료

# 1. 공격자 선정. -> 부서지지 않은 포탑중 가장 약한 포탑.
# 2. 공격자의 공격. -> 자신을 제외한 가장 강한 포탑 공격.
# 3. 포탑 부서짐. -> 공격력 0 이하 포탑 삭제.
# 4. 포탑 정비. -> 공격 당하지 않은 포탑, 공격하지 않은 포탑은 공격력 1씩 증가.

n,m,k = map(int,sys.stdin.readline().split())
field = []
for i in range(n):
    ttlis = []
    tlis = list(map(int,sys.stdin.readline().split()))
    for j in range(m):
        ttlis.append([tlis[j],0])
    field.append(ttlis)


def isbreak():
    key = 0
    for i in field:
        for j in i:
            if j[0] > 0:
                key += 1
    if key > 1:
        return True
    else:
        return False


def choose_cannon():
    maxxx = [-float('inf'),float('inf'),0,0,0] # 각각의 우선순위 두자. 1. 공격력(작을수록) 2. 최근 공격 시점(클수록) 3. x+y(클), 4. x(클), 5. y
    for i in range(n):
        for j in range(m):
            if field[i][j][0] > 0:
                maxxx = max(maxxx, [-field[i][j][0], field[i][j][1], i+j, j])
    
    return (maxxx[2] - maxxx[3], maxxx[3]) # 공격자의 y,x

def choose_enemy(att):
    y,x = att
    minnn = [float('inf'),-float('inf'),0,0,0] # 각각의 우선순위 두자. 1. 공격력(클) 2. 최근 공격 시점(작) 3. x+y(작), 4. x(작), 5. y
    for i in range(n):
        for j in range(m):
            if field[i][j][0] > 0 and not (i == y and j == x):
                minnn = min(minnn, [-field[i][j][0], field[i][j][1], i+j, j])
    
    return (minnn[2] - minnn[3], minnn[3]) # 피공격자의 y,x


def laser(att, oppo):
    # laser 의 조건: 포탑의 잔해를 피해 연결이 된다면 레이저, 아니면 포탄.
    DIR = [(0,1),(1,0),(0,-1),(-1,0)]
    power = field[att[0]][att[1]][0]

    # 먼저 bfs 로 연결 가능성 파악.
    queue = deque()
    queue.append((att[0],att[1],[att]))
    t_ans = []
    
    while queue:
        ty,tx,tq = queue.popleft()
        if (ty,tx) == oppo:
            t_ans = tq
            break
        else:
            for dy,dx in DIR:
                if field[(ty+dy)%n][(tx+dx)%m][0] > 0 and ((ty+dy)%n, (tx+dx)%m) not in tq:
                    queue.append(((ty+dy)%n,(tx+dx)%m, tq + [((ty+dy)%n, (tx+dx)%m)]))
    # 블락이 된다? -> 도착했다.
    consist = []
    if t_ans:
        # back(att[0],att[1])
        for tty,ttx in t_ans[1:-1]:
            field[tty][ttx][0] -= (power // 2)
        field[oppo[0]][oppo[1]][0] -= power
        return t_ans, True
    
    return [], False




def thorwing(att,oppo):
    DIR = [(0,1),(0,-1),(1,-1),(1,0),(1,1),(-1,-1),(-1,0),(-1,1)]
    consist = []
    # 공격 원점 피해
    power = field[att[0]][att[1]][0]
    field[oppo[0]][oppo[1]][0] -= power
    consist.append(oppo)
    consist.append(att)

    for dy,dx in DIR:
        ty,tx = oppo[0] + dy, oppo[1] + dx
        # 1. 공격자는 피해 없다.
        # 2. 부서진 포탑은 공격의 의미가 없다.
        if field[ty%n][tx%m][0] > 0 and not (ty%n == att[0] and tx%m == att[1]) :
            field[ty%n][tx%m][0] -= (power//2)
            consist.append((ty%n,tx%m))
        # 3. 만약 숫자가 넘어가면 넘어가서 피해를 입히자.

    return consist


def refresh_cannon(consist):
    for i in range(n):
        for j in range(m):
            if (i,j) not in consist and field[i][j][0] > 0:
                field[i][j][0] += 1 

count = 0
while k and isbreak():
    count += 1
    k -= 1
    # 공격자 선정.
    att = choose_cannon()
    # 공격받는 사람
    oppo = choose_enemy(att)
    # 마지막 공격 카운트.
    field[att[0]][att[1]][1] = count
    # 공격자 어드벤티지
    field[att[0]][att[1]][0] += (n+m)

    consist, is_t = laser(att,oppo)
    if not is_t:
        consist = thorwing(att,oppo)
    
    refresh_cannon(set(consist))

    # for i in field:
    #     print(i)
    # print()

maxxx = 0
for i in field:
    if max(i)[0] > maxxx:
        maxxx = max(i)[0]
print(maxxx)