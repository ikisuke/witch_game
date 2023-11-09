import pygame
import random
import time

# 初期設定
pygame.init()
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid Obstacles")

# 画像のロード
witch_img_original = pygame.image.load("witch.png")
candy_img_original = pygame.image.load("candy.png")
bg_img_original = pygame.image.load("background.png")

# キャンディーの画像サイズ調整
candy_img = pygame.transform.scale(candy_img_original, 
                                  (int(candy_img_original.get_width() // 20 * 1.5), 
                                   int(candy_img_original.get_height() // 20 * 1.5)))

# 魔女の画像サイズ調整
witch_img = pygame.transform.scale(witch_img_original, 
                                  (int(candy_img.get_width() * 2), 
                                   int(candy_img.get_height() * 2)))

# キャラクターと障害物の設定
char_width = witch_img.get_width()
char_height = witch_img.get_height()
char_pos = [WIDTH // 2 - char_width // 2, HEIGHT - char_height - 10]

obstacle_width = candy_img.get_width()
obstacle_height = candy_img.get_height()
obstacle_pos = [random.randint(0, WIDTH - obstacle_width), 0 - obstacle_height]
obstacle_speed = 10
player_speed = 5

# 背景スクロールの設定
bg_y1 = 0
bg_y2 = -HEIGHT

# ゲームの状態とタイマー
life = 3
score = 0
game_active = True
last_speed_increase_time = pygame.time.get_ticks()

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

clock = pygame.time.Clock()

while True:
    screen.blit(bg_img_original, (0, bg_y1))
    screen.blit(bg_img_original, (0, bg_y2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and char_pos[0] > 0:
            char_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and char_pos[0] + char_width < WIDTH:
            char_pos[0] += player_speed
        
        obstacle_pos[1] += obstacle_speed
        if obstacle_pos[1] > HEIGHT:
            obstacle_pos = [random.randint(0, WIDTH - obstacle_width), 0 - obstacle_height]
            score += 1
        
        # スピードアップの処理
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase_time > 3000:  # 3秒ごと
            obstacle_speed *= 1.2
            player_speed *= 1.2
            last_speed_increase_time = current_time
        
        # 背景のスクロール
        bg_y1 += 2
        bg_y2 += 2
        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT
        
        # キャラクターと障害物の描画
        screen.blit(witch_img, (char_pos[0], char_pos[1]))
        screen.blit(candy_img, (obstacle_pos[0], obstacle_pos[1]))
        
        # 当たり判定
        if (char_pos[0] < obstacle_pos[0] + obstacle_width and
            char_pos[0] + char_width > obstacle_pos[0] and
            char_pos[1] < obstacle_pos[1] + obstacle_height and
            char_pos[1] + char_height > obstacle_pos[1]):
            life -= 1
            obstacle_pos = [random.randint(0, WIDTH - obstacle_width), 0 - obstacle_height]
            
            # 画面を赤くするエフェクト
            screen.fill((255, 0, 0, 50))
            pygame.display.flip()
            time.sleep(0.2)
            
            if life == 0:
                game_active = False
        
        draw_text(f"Life: {life}", 36, (0, 255, 0), WIDTH // 4, 30)
        draw_text(f"Score: {score}", 36, (0, 255, 0), 3 * WIDTH // 4, 30)
    
    else:
        draw_text("Game Over!", 50, (255, 0, 0), WIDTH // 2, HEIGHT // 2)
        draw_text(f"Final Score: {score}", 40, (255, 255, 0), WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Press Space to restart", 30, (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 100)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = 0
                    life = 3
                    char_pos = [WIDTH // 2 - char_width // 2, HEIGHT - char_height - 10]
                    obstacle_pos = [random.randint(0, WIDTH - obstacle_width), 0 - obstacle_height]
                    obstacle_speed = 10
                    player_speed = 5
                    game_active = True

    pygame.display.flip()
    clock.tick(30)
