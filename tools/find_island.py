import numpy as np

ll = np.random.randint(2, size=[5,5])
_map = ll
print(_map)

h, w = _map.shape
visited = []
queue = []
end = 0

def find_island(_map, s, visited, queue, end):
    visited.append(s)
    if s[0] != h-1 and [s[0]+1, s[1]] not in visited and [s[0]+1, s[1]] not in queue and _map[s[0]+1, s[1]] == 1:
        queue.append([s[0]+1, s[1]])
        add = 1
        find_island(_map, [s[0]+1, s[1]], visited, queue, end)

    if s[0] != 0 and [s[0]-1, s[1]] not in visited and [s[0]-1, s[1]] not in queue and _map[s[0]-1, s[1]] == 1:
        queue.append([s[0]-1, s[1]])
        add = 1
        find_island(_map, [s[0]-1, s[1]], visited, queue, end)

    if s[1] != w-1 and [s[0], s[1]+1] not in visited and [s[0], s[1]+1] not in queue and _map[s[0], s[1]+1] == 1:
        queue.append([s[0], s[1]+1])
        add = 1
        find_island(_map, [s[0], s[1]+1], visited, queue, end)

    if s[1] != 0 and [s[0], s[1]-1] not in visited and [s[0], s[1]-1] not in queue and _map[s[0], s[1]-1] == 1:
        queue.append([s[0], s[1]-1])
        add = 1
        find_island(_map, [s[0], s[1]-1], visited, queue, end)
    queue.remove(s)

    if queue == []:
        end += 1

count = 0
for i in range(h):
    for j in range(w):
        s = [i, j]
        if _map[i, j] == 1 and [i, j] not in visited:
            print(s)
            print(visited)
            print(queue)
            queue.append(s)
            find_island(_map, s, visited, queue, end)
            count += 1
            print(count)
        else:
            visited.append(s)
