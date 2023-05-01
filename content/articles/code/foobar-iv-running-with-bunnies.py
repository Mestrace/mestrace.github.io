def floyd_warshall(times):
    n = len(times)
    dist = [list(t) for t in times] # list.copy
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


result = None

def solution(times, times_limit):
    # reset
    # I hate python2 foobar should consider use python3
    global result
    result = []
    
    # computes the shortest distance by floyd warshall
    dist = floyd_warshall(times)
    
    # if there are negative cycle, we can always hit
    # it to add more time and save all bunnies
    for i in range(len(times)):
        if dist[i][i] < 0:
            return [i for i in range(len(times) - 2)]
    
    def bt(dist, time_limit, i, visited, bunnies):
        # only for python3
        # nonlocal result
        
        if time_limit < -1000:
            return
        
        global result
        if i == len(dist) - 1:
            if time_limit >= 0 and len(bunnies) > len(result):
                result = list(bunnies) # list.copy
            return

        if visited[i]:
            return
        visited[i] = True
        bunnies.append(i - 1)

        for j in range(0, len(dist)):
            if i == j:
                continue
            bt(dist, time_limit - dist[i][j], j, visited, bunnies)
        
        bunnies.pop()
        visited[i] = False
    
    visited = [False] * len(times)
    visited[0] = True
    # try each bunny as starting point
    for i in range(1, len(dist) - 1):
        bt(dist, times_limit - dist[0][i], i, visited, [])
    
    return sorted(result)