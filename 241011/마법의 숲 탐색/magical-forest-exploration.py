import sys
from collections import deque

ADD_DIR = [(0,0),(0,1),(1,0),(-1,0),(0,-1)]

def m_south(center, ex):
    return (center[0]+1, center[1]), ex

def m_west(center, ex):
    return (center[0]+1, center[1]-1), (ex - 1) % 4

def m_east(center, ex):
    return (center[0]+1, center[1]+1), (ex + 1) % 4

def v_south(center):
    y,x = center[0], center[1]
    if y + 2 < r + 3:
        if not field[y+2][x] and not field[y+1][x-1] and not field[y+1][x+1]:
            return True
        else:
            return False
    else:
        return False

def v_west(center):
    y,x = center[0], center[1]
    if y + 2 < r + 3 and 0 <= x - 2:
        if not field[y][x-2] and not field[y-1][x-1] and not field[y+1][x-2] and not field[y+1][x-1] and not field[y+2][x-1]:
            return True
        else:
            return False
    else:
        return False

def v_east(center):
    y,x = center[0], center[1]
    if y + 2 < r + 3 and x + 2 < c:
        if not field[y][x+2] and not field[y-1][x+1] and not field[y+1][x+1] and not field[y+1][x+2] and not field[y+2][x+1]:
            return True
        else:
            return False
    else:
        return False

def reset():
    global field
    field = [[False] * c for _ in range(r+3)]


def field_adder(center, ex, fill):
    for dy, dx in ADD_DIR:
        if not 3 <= center[0] + dy < r+3:
            return False

    for dy, dx in ADD_DIR:
        field[center[0] + dy][center[1] + dx] = fill
    
    field[center[0] + DIR[ex][0]][center[1] + DIR[ex][1]] = -fill # 출구 표시
    return True

# bfs를 이용해 가장 깊은곳으로
def goto_end(now_y, now_x, fill):
    visited = [[False] * (c) for _ in range(r+3)]
    visited[now_y][now_x] = True

    queue = deque([(now_y, now_x, fill)])
    
    southest = 0

    while queue:
        n_y, n_x, now = queue.popleft()
        southest = max(n_y, southest)
        for dy,dx in DIR:
            if 3 <= n_y + dy < r+3 and 0 <= n_x + dx < c and not visited[n_y+dy][n_x+dx]:
                if field[n_y][n_x] != -now: # 출구 아닐때 
                    if field[n_y+dy][n_x+dx] == now:
                        queue.append((n_y+dy, n_x+dx, now)) # 같은숫자면 계속 가
                        visited[n_y+dy][n_x+dx] = True
                    
                    elif field[n_y+dy][n_x+dx] == -now:
                        queue.append((n_y+dy, n_x+dx, now))
                        visited[n_y+dy][n_x+dx] = True
                
                else: # 출구일때 
                    if field[n_y+dy][n_x+dx] != False: 
                        queue.append((n_y+dy, n_x+dx, field[n_y+dy][n_x+dx])) # 다음위치 받아들이기
                        visited[n_y+dy][n_x+dx] = True
                    
    
    return southest
                


DIR = [(-1,0),(0,1), (1,0), (0,-1)] # 북 동 남 서
r,c,k = map(int,sys.stdin.readline().split())

field = [[False] * c for _ in range(r+3)] # 차있는지 안차있는지 관리.

ans = 0

for i in range(1,k+1):
    center, ex = map(int,sys.stdin.readline().split())
    center = (1,center-1)
    
    while True:
        # 남쪽은 center 기준 (2,0),(1,1),(1,-1)가 비어있어야 한다.
        # 만약 남쪽? -> ex 그대로
        if v_south(center):
            center, ex = m_south(center, ex)


        # 서쪽은 center 기준 (0,-1),(1,0),(1,-1),(1,-2),(2,-1) 가 비어있어야 한다.
        # 만약 서쪽? -> ex DIR 기준 -1
        elif v_west(center):
            center, ex = m_west(center, ex)


        # 동쪽은 center 기준 (0,1),(1,0),(1,1),(1,2),(2,1) 가 비어있어야 한다.
        # 만약 동쪽? -> ex DIR 기준 +1
        elif v_east(center):
            center, ex = m_east(center, ex)
        
        else:
            break


    # 골램 배치
    key = field_adder(center, ex, i)
    # 다 정리후 정령의 이동
    if key:
        ans += goto_end(center[0], center[1],i) - 2
    else:
        reset()

print(ans)