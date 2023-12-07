import pygame
import sys
import random
from collections import deque
import heapq
from queue import PriorityQueue
pygame.init()
WIDTH, HEIGHT = 500, 300
global empty_tile
TILE_SIZE = 300 // 3
BACKGROUND_COLOR = (139, 139, 122)
TILE_COLOR = (255, 204, 153)
step_count = 0
BUTTON_COLOR = (139, 139, 131) 
BUTTON_HOVER_COLOR = (245, 255, 250)
Grey=	(192,192,192)
button_x_1 = 305 
button_y_1 = 10  
BUTTON_WIDTH_1 = 87 
BUTTON_HEIGHT_1 = 30  
button_x_2 = 305  
button_y_2 = 45  
BUTTON_WIDTH_2 = 87
BUTTON_HEIGHT_2 = 30 
button_x_3 = 305  
button_y_3 = 80  
BUTTON_WIDTH_3 = 87 
BUTTON_HEIGHT_3 = 30 
button_x_4 = 305  
button_y_4 = 115  
BUTTON_WIDTH_4 = 87
BUTTON_HEIGHT_4 = 30 
button_x_5 = 305  
button_y_5 = 150  
BUTTON_WIDTH_5 = 87
BUTTON_HEIGHT_5 = 30 
button_x_6 = 305  
button_y_6 = 185  
BUTTON_WIDTH_6 = 87
BUTTON_HEIGHT_6 = 30 
button_x_7 = 305  
button_y_7 = 185+35 
BUTTON_WIDTH_7 = 87
BUTTON_HEIGHT_7 = 30 
button_x_8 = 407
button_y_8 = 10  
BUTTON_WIDTH_8 = 87 
BUTTON_HEIGHT_8 = 30 
node_count = 0
font = pygame.font.Font(None, 25)
image = pygame.image.load("pngwing.com.png")
image = pygame.transform.scale(image, (300, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Puzzle")
numbers = list(range(0, 9))
random.shuffle(numbers)
current_state = [numbers[i:i + 3] for i in range(0, len(numbers), 3)]
initial_current_state = [row[:] for row in current_state]
initial_state = [[0,1,2], [3,4,5], [6,7,8]]
# initial_state = [[2, 8, 1], [0, 4, 3], [7, 6, 5]] 
# current_state= [[ 1, 2, 3], [8, 0, 4], [7, 6, 5]]
value_to_find = 0
found = False
row, col = None, None
menu_part = pygame.Rect(300, 0, 100, 400)
menu_color = (152, 251, 152)
for i in range(3):
    for j in range(3):
        if current_state[i][j] == value_to_find:
            found = True
            row, col = i, j
            break
empty_tile = [col, row]
initial_empty_tile = list(empty_tile)
empty_color=(250, 240, 230)
def draw_image(tile, x, y): 
    pygame.draw.rect(screen, TILE_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)) 
    font = pygame.font.Font(None, 36)
    text = font.render(str(tile), True, (0, 0, 0))
    text_rect = text.get_rect(center=(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2))
    screen.blit(text, text_rect)
def solve_puzzle_BFS(current_state, initial_state):
    queue = deque([(current_state, [])])
    visited = set([tuple(map(tuple, current_state))])
    global node_count
    node_count = 0
    while queue:
        node_count += 1
        state, path = queue.popleft()
        if state == initial_state:
            return path
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                if tuple(map(tuple, new_state)) not in visited:
                    queue.append((new_state, new_path))
                    visited.add(tuple(map(tuple, new_state)))   
def solve_puzzle_DFS(current_state, initial_state, max_depth):
    stack = [(current_state, [])]
    visited = set()
    global node_count
    node_count = 0
    while stack:
        node_count += 1
        state, path = stack.pop()
        if state == initial_state:
            return path
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                if tuple(map(tuple, new_state)) not in visited and len(new_path) <= max_depth:
                    stack.append((new_state, new_path))
                    visited.add(tuple(map(tuple, new_state)))
    return None
def solve_puzzle_UCS(current_state, initial_state):
    # Khởi tạo hàng đợi ưu tiên với chi phí ban đầu là 0
    queue = [(0, current_state, [])]
    visited = set()
    global node_count
    node_count = 0
    while queue:
        node_count += 1
        cost, state, path = heapq.heappop(queue)
        if state == initial_state:
            return path
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                new_cost = cost + 1
                if tuple(map(tuple, new_state)) not in visited:
                    heapq.heappush(queue, (new_cost, new_state, new_path))
                    visited.add(tuple(map(tuple, new_state)))
    return None
def solve_puzzle_ID(current_state, initial_state):
    depth = 0
    while True:
        result = depth_limited_DFS(current_state, initial_state, depth)
        if result is not None:
            return result
        depth += 1
def depth_limited_DFS(current_state, initial_state, max_depth):
    stack = [(current_state, [])]
    visited = set()
    global node_count
    node_count = 0
    while stack:
        node_count += 1
        state, path = stack.pop()
        if state == initial_state:
            return path
        if len(path) >= max_depth:
            continue
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]

                if tuple(map(tuple, new_state)) not in visited:
                    stack.append((new_state, new_path))
                    visited.add(tuple(map(tuple, new_state)))
    return None
def heuristic(state, goal_state):
    # Hàm heuristic, ở đây bạn có thể sử dụng Manhattan distance hoặc Euclidean distance
    h = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j]:
                h += 1
    return h
def find_empty_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
def solve_puzzle_Astar(current_state, goal_state):
    priority_queue = PriorityQueue()
    priority_queue.put((heuristic(current_state, goal_state), 0, current_state, []))
    visited = set([tuple(map(tuple, current_state))])
    global node_count
    node_count = 0

    while not priority_queue.empty():
        node_count += 1
        _, cost, state, path = priority_queue.get()

        if state == goal_state:
            return path

        row, col = find_empty_position(state)

        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                if tuple(map(tuple, new_state)) not in visited:
                    visited.add(tuple(map(tuple, new_state)))
                    new_cost = cost + 1
                    priority_queue.put((new_cost + heuristic(new_state, goal_state), new_cost, new_state, new_path))
def solve_puzzle_greedy(current_state, initial_state):
    queue = [(heuristic(current_state, initial_state), current_state, [])]
    visited = set()
    global node_count
    node_count = 0
    while queue:
        node_count += 1
        _, state, path = heapq.heappop(queue)
        if state == initial_state:
            return path
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                if tuple(map(tuple, new_state)) not in visited:
                    heapq.heappush(queue, (heuristic(new_state, initial_state), new_state, new_path))
                    visited.add(tuple(map(tuple, new_state)))
    return None
def solve_puzzle_HillClimbing(current_state, initial_state, max_depth):
    stack = [(current_state, [])]
    visited = set()
    global node_count
    node_count = 0
    while stack:
        node_count += 1
        state, path = stack.pop()
        if state == initial_state:
            return path
        row, col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
        best_state = None
        best_heuristic = float('inf')
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_state = [list(row) for row in state]
                new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
                new_path = path + [(new_row, new_col)]
                if tuple(map(tuple, new_state)) not in visited and len(new_path) <= max_depth:
                    heuristic_value = heuristic(new_state, initial_state)  # Calculate the heuristic value
                    if heuristic_value < best_heuristic:
                        best_heuristic = heuristic_value
                        best_state = new_state
        if best_state is not None:
            stack.append((best_state, path + [(new_row, new_col)]))
            visited.add(tuple(map(tuple, best_state)))
    return None
def handle_events():
    global step_count, empty_tile, current_state, row, col, value_to_find
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and empty_tile[1] > 0:
                current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                empty_tile[1] -= 1
                step_count+=1
            elif event.key == pygame.K_DOWN and empty_tile[1] < 2:
                current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                empty_tile[1] += 1 
                step_count += 1
            elif event.key == pygame.K_LEFT and empty_tile[0] > 0:
                current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                empty_tile[0] -= 1
                step_count += 1
            elif event.key == pygame.K_RIGHT and empty_tile[0] < 2:
                current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                empty_tile[0] += 1
                step_count += 1
        if event.type == pygame.MOUSEBUTTONDOWN:           
            if button_x_1 < event.pos[0] < button_x_1 + BUTTON_WIDTH_1 and button_y_1 < event.pos[1] < button_y_1 + BUTTON_HEIGHT_1:
                path = solve_puzzle_BFS(current_state, initial_state)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0)) 
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0)) 
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_2 < event.pos[0] < button_x_2 + BUTTON_WIDTH_2 and button_y_2 < event.pos[1] < button_y_2 + BUTTON_HEIGHT_2:
                path = solve_puzzle_DFS(current_state, initial_state, 100)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C")  
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0))  
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2)) 
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_3 < event.pos[0] < button_x_3 + BUTTON_WIDTH_3 and button_y_3 < event.pos[1] < button_y_3 + BUTTON_HEIGHT_3:
                path = solve_puzzle_UCS(current_state, initial_state)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy")  
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0))  
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2)) 
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_4 < event.pos[0] < button_x_4 + BUTTON_WIDTH_4 and button_y_4 < event.pos[1] < button_y_4 + BUTTON_HEIGHT_4:
                path = solve_puzzle_ID(current_state, initial_state)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy")  
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0)) 
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10) 
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0)) 
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2)) 
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_5 < event.pos[0] < button_x_5 + BUTTON_WIDTH_5 and button_y_5 < event.pos[1] < button_y_5 + BUTTON_HEIGHT_5:
                path = solve_puzzle_Astar(current_state, initial_state)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C")  
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0)) 
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0))  
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_6 < event.pos[0] < button_x_6 + BUTTON_WIDTH_6 and button_y_6 < event.pos[1] < button_y_6 + BUTTON_HEIGHT_6:
                path = solve_puzzle_greedy(current_state, initial_state)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0))  
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    
            elif button_x_7 < event.pos[0] < button_x_7 + BUTTON_WIDTH_7 and button_y_7 < event.pos[1] < button_y_7 + BUTTON_HEIGHT_7:
                # print(current_state )
                # print(empty_tile)
                current_state = [row[:] for row in initial_current_state]
                empty_tile = list(initial_empty_tile)
                # print(current_state )
                # print(empty_tile)
                step_count=0
                screen.fill(BACKGROUND_COLOR)
                for y in range(3):
                    for x in range(3):
                        tile = current_state[y][x]
                        if tile != 0:
                            draw_image(tile, x, y) 
                screen.fill(menu_color, menu_part) 
                text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
                text_rect = text.get_rect()
                text_rect.bottomright = (390, 300-10) 
                screen.blit(text, text_rect)   
                draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C")
            elif button_x_8 < event.pos[0] < button_x_8 + BUTTON_WIDTH_8 and button_y_8 < event.pos[1] < button_y_8 + BUTTON_HEIGHT_8:
                path = solve_puzzle_HillClimbing(current_state, initial_state, 99999)
                print("Số lượng đỉnh đã duyệt qua:", node_count)
                if path:                   
                    for move in path:  
                        pygame.time.wait(250)
                        screen.fill(BACKGROUND_COLOR)
                        for y in range(3):
                            for x in range(3):
                                tile = current_state[y][x]
                                if tile != 0:
                                    draw_image(tile, x, y)   
                        screen.fill(menu_color, menu_part)
                        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
                        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
                        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
                        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
                        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
                        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
                        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
                        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
                        text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
                        text_rect = text.get_rect()
                        text_rect.bottomright = (390, 300-10)  
                        screen.blit(text, text_rect)
                        pygame.display.update()
                        empty_row, empty_col = empty_tile[1], empty_tile[0]
                        move_row, move_col = move
                        if move_row-empty_row==-1 and move_col-empty_col==0 and empty_tile[1] > 0:                            
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] - 1][empty_tile[0]] = current_state[empty_tile[1] - 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] -= 1
                            step_count+=1                           
                        elif move_row-empty_row==1 and move_col-empty_col==0 and empty_tile[1] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1] + 1][empty_tile[0]] = current_state[empty_tile[1] + 1][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[1] += 1 
                            step_count += 1
                            screen.fill(BACKGROUND_COLOR)                           
                        elif move_row-empty_row==0 and move_col-empty_col==-1 and empty_tile[0] > 0:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] - 1] = current_state[empty_tile[1]][empty_tile[0] - 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] -= 1
                            step_count += 1                           
                        elif move_row-empty_row==0 and move_col-empty_col==1 and empty_tile[0] < 2:
                            current_state[empty_tile[1]][empty_tile[0]], current_state[empty_tile[1]][empty_tile[0] + 1] = current_state[empty_tile[1]][empty_tile[0] + 1], current_state[empty_tile[1]][empty_tile[0]]
                            empty_tile[0] += 1
                            step_count += 1                            
                else:
                    print("Không tìm thấy lời giải")
                    text = font.render("Can't solve", True, (255, 0, 0))  
                    text_rect = text.get_rect()
                    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  
                    screen.blit(text, text_rect) 
                    pygame.display.flip()
                    pygame.time.wait(1000)    
                pygame.display.update()
def is_win():
    for i in range(3):
        for j in range(3):
            if current_state[i][j] != initial_state[i][j]:
                return False
    return True
def draw_button(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT,x):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, Grey, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    mouse_click = pygame.mouse.get_pressed()
    if button_x < mouse_x < button_x + BUTTON_WIDTH and button_y < mouse_y < button_y + BUTTON_HEIGHT:
        if mouse_click[0]: 
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text = font.render(x, True, (0,0,0))
    text_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH / 2, button_y + BUTTON_HEIGHT / 2))
    screen.blit(button_text, text_rect)
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    for y in range(3):
        for x in range(3):
            tile = current_state[y][x]
            if tile != 0:
                draw_image(tile, x, y) 
    screen.fill(menu_color, menu_part) 
    text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
    text_rect = text.get_rect()
    text_rect.bottomright = (390, 300-10) 
    screen.blit(text, text_rect)   
    draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
    draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
    draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
    draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
    draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
    draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
    draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
    draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
    pygame.display.update()
    handle_events()
    if is_win():
        pygame.time.wait(500)
        screen.fill(BACKGROUND_COLOR)
        for y in range(3):
            for x in range(3):
                tile = current_state[y][x]
                if tile != 0:
                    draw_image(tile, x, y)   
        screen.fill(menu_color, menu_part)
        text = font.render(f"Step: {step_count}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.bottomright = (390, 300-10) 
        screen.blit(text, text_rect)
        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset")  
        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C")       
        #screen.fill(menu_color, menu_part) 
        text = font.render("You win!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        print("You win!")  
        pygame.time.wait(3000)
        current_state = [row[:] for row in initial_current_state]
        empty_tile = list(initial_empty_tile)
        # print(current_state )
        # print(empty_tile)
        step_count=0
        screen.fill(BACKGROUND_COLOR)
        for y in range(3):
            for x in range(3):
                tile = current_state[y][x]
                if tile != 0:
                    draw_image(tile, x, y) 
        screen.fill(menu_color, menu_part) 
        text = font.render(f"Step: {step_count}", True, (0, 0, 0))  
        text_rect = text.get_rect()
        text_rect.bottomright = (390, 300-10) 
        screen.blit(text, text_rect)   
        draw_button(button_x_1, button_y_1, BUTTON_WIDTH_1, BUTTON_HEIGHT_1, "BFS")
        draw_button(button_x_2, button_y_2, BUTTON_WIDTH_2, BUTTON_HEIGHT_2, "DFS")  
        draw_button(button_x_3, button_y_3, BUTTON_WIDTH_3, BUTTON_HEIGHT_3, "UCS") 
        draw_button(button_x_4, button_y_4, BUTTON_WIDTH_4, BUTTON_HEIGHT_4, "ID")
        draw_button(button_x_5, button_y_5, BUTTON_WIDTH_5, BUTTON_HEIGHT_5, "A*")
        draw_button(button_x_6, button_y_6, BUTTON_WIDTH_6, BUTTON_HEIGHT_6, "Greedy") 
        draw_button(button_x_7, button_y_7, BUTTON_WIDTH_7, BUTTON_HEIGHT_7, "Reset") 
        draw_button(button_x_8, button_y_8, BUTTON_WIDTH_8, BUTTON_HEIGHT_8, "Hill.C") 
        pygame.display.update()   
pygame.quit()
sys.exit()