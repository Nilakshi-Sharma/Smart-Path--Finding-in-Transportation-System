from collections import deque

# Maze: 0 = path, 1 = wall
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
]

# Directions: right, down, left, up
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def bfs(maze, start, target):
    queue = deque([(start, [start])])  # (position, path)
    visited = [[False] * len(maze[0]) for _ in range(len(maze))]
    visited[start[0]][start[1]] = True

    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == target:
            return path  

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and not visited[nx][ny] and maze[nx][ny] == 0:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited[nx][ny] = True

    return None  #  if no path found

start = (0, 0)
target = (4, 4)
path = bfs(maze, start, target)
print("Path:", path if path else "No path found.")
