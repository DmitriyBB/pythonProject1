import pygame
import random

pygame.init()

# окно
screen_width = 600
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("rocket")

# загрузка звуков
pygame.mixer.music.load('файл_звука_фона.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('файл_звука_проигрыша.wav')

# игрок
player_width = 50
player_height = 50
player_x = 270
player_y = 580
player_speed = 5
player_img = pygame.image.load('rocket.png')
player = pygame.Rect(player_x, player_y, player_width, player_height)
player_img_left = pygame.image.load('player_img_left.png')
player_img_right = pygame.image.load('player_img_right.png')

# препятствия
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_img = pygame.image.load('meteor.png')
obstacles = []

# задний фон
background_speed = 3
background_image = pygame.image.load('background.png')
background_rect1 = pygame.Rect(0, 0, screen_width, screen_height)
background_rect2 = pygame.Rect(0, -screen_height, screen_width, screen_height)
# игровые переменные
is_running = True
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)
black_hole_width = 50
black_hole_height = 50
black_hole_speed = 8
black_hole_img = pygame.image.load('black_hole.png')
black_holes = []


def show_menu():
    menu_font = pygame.font.Font(None, 50)
    menu_text = menu_font.render("Press SPACE to start", True, (255, 255, 255))
    menu_text_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(menu_text, menu_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


show_menu()


def game_loop():
    global is_running, score
    is_running = True
    score = 0

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player.x -= player_speed
            screen.blit(player_img_left, player)
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player.x += player_speed
            screen.blit(player_img_right, player)

        # обновление заднего фона
        background_rect1.y += background_speed
        background_rect2.y += background_speed

        if background_rect1.y > screen_height:
            background_rect1.y = -screen_height
        if background_rect2.y > screen_height:
            background_rect2.y = -screen_height

        # обновление препятствий
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > screen_height:
                obstacles.remove(obstacle)
                score += 10

        # создание новых препятствий
        if random.randint(0, 100) < 2:
            obstacle_x = random.randint(0, screen_width - obstacle_width)
            obstacle_y = 0 - obstacle_height
            obstacle = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
            obstacles.append(obstacle)

        # обновление чёрных дыр
        for black_hole in black_holes:
            black_hole.y += black_hole_speed
            if black_hole.y > screen_height:
                black_holes.remove(black_hole)

        # создание новых чёрных дыр с меньшей вероятностью
        if random.randint(0, 200) == 0:
            black_hole_x = random.randint(0, screen_width - black_hole_width)
            black_hole_y = 0 - black_hole_height
            black_hole = pygame.Rect(black_hole_x, black_hole_y, black_hole_width, black_hole_height)
            black_holes.append(black_hole)

        # проверка на встречу с чёрной дырой
        for black_hole in black_holes:
            if player.colliderect(black_hole):
                is_running = False

        # проверка на столкновения с препятствиями
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                is_running = False

        screen.blit(background_image, background_rect1)
        screen.blit(background_image, background_rect2)

        for obstacle in obstacles:
            screen.blit(obstacle_img, obstacle)

        # отображение чёрных дыр
        for black_hole in black_holes:
            screen.blit(black_hole_img, black_hole)

        screen.blit(player_img, player)

        score_text = font.render("score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()

        time_passed = clock.tick(60)

    # конец игры
    game_over_sound.play()
    game_over_text = font.render("game over", True, (250, 250, 250))
    return_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2, 150, 50)
    exit_button = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 70, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return game_loop()

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        pygame.draw.rect(screen, (255, 0, 0), return_button)
        pygame.draw.rect(screen, (255, 0, 0), exit_button)

        return_text = font.render("Return", True, (0, 0, 0))
        screen.blit(return_text, (screen_width // 2 - 45, screen_height // 2 + 10))

        exit_text = font.render("Exit", True, (0, 0, 0))
        screen.blit(exit_text, (screen_width // 2 - 20, screen_height // 2 + 80))
        pygame.mixer.music.stop()
        pygame.display.update()


game_loop()

pygame.quit()
exit()
