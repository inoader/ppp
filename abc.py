import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 1000, 800  # 增加高度以显示分数
TILE_SIZE = 100
ROWS, COLS = 7, 10
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BG_COLOR = (200, 200, 200)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("噗了个噗")

# 加载图案图片
patterns = [pygame.image.load(f"bear{i}.gif") for i in range(0, 12)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 加载支持中文的字体文件
font_path = "simhei.ttf"  # 确保字体文件在项目目录中
font = pygame.font.Font(font_path, 36)

# 初始化游戏板，确保每种图片的数量为偶数
def init_board():
    num_patterns = len(patterns)
    num_tiles = ROWS * COLS

    # 创建一个包含偶数个每种图片的列表
    tiles = []

    # 如果图片数量不够，补充剩余的图片
    while len(tiles) < num_tiles:
        a = random.sample(range(num_patterns),1)
        tiles.extend(a)
        tiles.extend(a)

    # 随机打乱列表
    random.shuffle(tiles)

    # 填充到游戏板中
    board = []
    for row in range(ROWS):
        board.append(tiles[row * COLS:(row + 1) * COLS])
    return board

board = init_board()
selected = []
score = 0

# 绘制游戏板和分数
def draw_board():
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != -1:  # -1 表示该位置已被消除
                screen.blit(patterns[board[row][col]], (col * TILE_SIZE, row * TILE_SIZE))
                if (row, col) in selected:
                    pygame.draw.rect(screen, RED, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)
    
    # 显示分数
    score_text = font.render(f"分数: {score}", True, BLACK)
    screen.blit(score_text, (10, HEIGHT - 50))
    
    pygame.display.flip()

# 检查匹配
def check_match():
    global score
    if len(selected) == 2:
        (row1, col1), (row2, col2) = selected
        if (row1, col1) != (row2, col2) and board[row1][col1] == board[row2][col2]:
            board[row1][col1] = -1  # 设置为 -1 表示该位置已被消除
            board[row2][col2] = -1
            score += 1
        else:
            score -= 1  # 消除失败扣分
        selected.clear()

# 检查游戏是否结束
def check_game_over():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] != -1:
                return False
    return True

# 显示开始界面
def show_start_screen():
    screen.fill(BG_COLOR)
    start_text = font.render("按任意键开始游戏", True, BLACK)
    text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, text_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# 显示游戏结束界面
def show_game_over_screen():
    screen.fill(BG_COLOR)
    game_over_text = font.render("游戏结束", True, BLACK)
    pygame.display.flip()
    pygame.time.wait(3000)  # 等待3秒

# 显示通关界面
def show_victory_screen():
    screen.fill(BG_COLOR)
    victory_text = font.render("恭喜通关！", True, BLACK)
    text_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(victory_text, text_rect)
    score_text = font.render(f"分数: {score}", True, BLACK) 
    screen.blit(score_text, (WIDTH //2 -80, HEIGHT //2 +100))
    pygame.display.flip()
    pygame.time.wait(3000)  # 等待3秒

# 主游戏循环
def main():
    global selected
    show_start_screen()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
                if board[row][col] != -1:  # 仅当该位置未被消除时才处理点击
                    selected.append((row, col))
                    if len(selected) == 2:
                        check_match()

        draw_board()
        if check_game_over():
            show_victory_screen()
            running = False

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()