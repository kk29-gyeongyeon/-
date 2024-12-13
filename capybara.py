import pygame
import sys
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("점프바라 어드벤처")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 배경 음악 및 효과음 설정
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
jump_sound = pygame.mixer.Sound("jump_sound.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
game_clear_sound = pygame.mixer.Sound("game_clear.wav")


# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 점수 초기화
score = 0

# 이미지 로드
background = pygame.image.load("background2.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

main_screen = pygame.image.load("main_screen.png")
main_screen = pygame.transform.scale(main_screen, (WIDTH, HEIGHT))

start_button = pygame.image.load("start.png")
start_button = pygame.transform.scale(start_button, (190, 90))
start_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 18))

how_button = pygame.image.load("how.png")
how_button = pygame.transform.scale(how_button, (190, 90))
how_rect = how_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

game_over_image = pygame.image.load("game_over.png")
game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

game_clear_image = pygame.image.load("game_clear.png")
game_clear_image = pygame.transform.scale(game_clear_image, (WIDTH, HEIGHT))

information_image = pygame.image.load("information.png")
information_image = pygame.transform.scale(information_image, (WIDTH, HEIGHT))



# 플레이어 설정
player_image = pygame.image.load("player_sprite3.png")
player_image = pygame.transform.scale(player_image, (80, 80))
player_x, player_y = 100, HEIGHT - 80 - 10
player_velocity_y = 0
player_speed = 5
player_jump = -15
gravity = 0.8
is_jumping = False

# 장애물 설정
obstacle_image = pygame.image.load("bear.png")
obstacle_image = pygame.transform.scale(obstacle_image, (90, 90))
obstacle_speed = 5
obstacles = [{"x": WIDTH + i * 300, "y": HEIGHT - 90 - 10} for i in range(3)]

# 코인 설정
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (30, 30))
coins = [{"x": WIDTH + i * 500, "y": HEIGHT - 30} for i in range(2)]

# 난이도 증가 설정
difficulty_timer = 0

# 게임 상태
game_state = "main_menu"

# 보스 설정
boss_image = pygame.image.load("ice_wolf.png")
boss_image = pygame.transform.scale(boss_image, (120, 110))
boss_x, boss_y = WIDTH - 120 - 10, HEIGHT - 110 - 10  # 화면 중앙에 생성
boss_speed = 3
boss_direction = -1  # 좌우로 움직이는 방향
boss_health = 5
boss_active = False
boss_attack_timer = 0
ice_beams = []

# 얼음빔 설정
ice_beam_image = pygame.image.load("ice_beam.png")
ice_beam_image = pygame.transform.scale(ice_beam_image, (40, 20))

# 플레이어 상태
is_disabled = False
disable_timer = 0


def reset_game():
    """게임 상태 초기화"""
    global player_x, player_y, player_velocity_y, is_jumping, obstacles, coins, score, obstacle_speed, boss_active, boss_health, boss_x, boss_y, ice_beams, boss_image
    player_x, player_y = 100, HEIGHT - 50
    player_velocity_y = 0
    is_jumping = False
    obstacles = [{"x": WIDTH + i * 300, "y": HEIGHT - 50} for i in range(3)]
    coins = [{"x": WIDTH + i * 500, "y": HEIGHT - 80} for i in range(2)]
    score = 0
    obstacle_speed = 5
    boss_active = False
    boss_health = 3
    boss_x, boss_y = WIDTH // 2, HEIGHT - 110 - 10
    ice_beams.clear()
    boss_image = pygame.transform.scale(pygame.image.load("ice_wolf.png"), (120, 110))


def resize_boss():
    """보스를 밟을 때 크기를 줄이는 함수"""
    global boss_image
    boss_width, boss_height = boss_image.get_size()
    new_width = max(40, boss_width - 20)
    new_height = max(40, boss_height - 20)
    boss_image = pygame.transform.scale(boss_image, (new_width, new_height))


# 게임 루프
running = True
while running: 
# 게임 상태 전환 로직
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 게임 종료
        elif event.type == pygame.MOUSEBUTTONDOWN:
             if game_state == "main_menu":
                if start_rect.collidepoint(event.pos):  # 시작 버튼 클릭 시
                    reset_game()
                    game_state = "game_active"  # 게임 상태를 활성 상태로 변경
                elif how_rect.collidepoint(event.pos):  # How to Play 버튼 클릭 시
                    game_state = "how_to_play"  # 튜토리얼 화면으로 이동
        elif event.type == pygame.KEYDOWN:
            if game_state == "game_active" and event.key == pygame.K_ESCAPE:
                game_state = "paused"  # 게임을 일시 정지
            elif game_state == "paused" and event.key == pygame.K_ESCAPE:
                game_state = "game_active"  # 일시 정지 상태에서 게임으로 돌아가기
            elif game_state == "how_to_play" and event.key == pygame.K_ESCAPE:
                game_state = "main_menu"  # "how_to_play"에서 ESC 눌렀을 때 메인 화면으로 돌아가기
            elif game_state == "game_over" and event.key == pygame.K_RETURN:
                reset_game()
                game_state = "game_active"

    keys = pygame.key.get_pressed()

    if game_state == "main_menu":
        screen.blit(main_screen, (0, 0))
        screen.blit(start_button, start_rect.topleft)
        screen.blit(how_button, how_rect.topleft)

    elif game_state == "how_to_play":
        screen.blit(information_image, (0,0))
        how_text1 = font.render("<- , -> to move", True, BLACK)
        how_text2 = font.render("Jump = Spacebar", True, BLACK)
        how_text3 = font.render("Esc to pause", True, BLACK)
        screen.blit(how_text1, (WIDTH // 2 - how_text1.get_width() // 2, HEIGHT // 3))
        screen.blit(how_text2, (WIDTH // 2 - how_text2.get_width() // 2, HEIGHT // 3 + 40))
        screen.blit(how_text3, (WIDTH // 2 - how_text3.get_width() // 2, HEIGHT // 3 + 80))

    elif game_state == "game_active":
        screen.blit(background, (0, 0))

        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if not is_disabled and keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = player_jump
            is_jumping = True
            jump_sound.play()

        player_velocity_y += gravity
        player_y += player_velocity_y

        if player_y >= HEIGHT - 50:
            player_y = HEIGHT - 50
            is_jumping = False

        if not boss_active:
            for obstacle in obstacles:
                obstacle["x"] -= obstacle_speed
                if obstacle["x"] < -50:
                    obstacle["x"] = WIDTH + random.randint(100, 300)

            for coin in coins:
                coin["x"] -= obstacle_speed
                if coin["x"] < -30:
                    coin["x"] = WIDTH + random.randint(500, 800)
        else:
            obstacles = []

        difficulty_timer += 1
        if difficulty_timer >= 600:
            obstacle_speed += 1
            difficulty_timer = 0
#플레이어 충돌 검사
        player_rect = pygame.Rect(player_x, player_y, 50, 50)  # 플레이어의 현재 위치를 Rect 객체로 정의
        for obstacle in obstacles:  # 장애물들과 충돌 검사
            obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], 50, 50)   # 장애물을 Rect 객체로 정의
            if player_rect.colliderect(obstacle_rect):  # 플레이어와 장애물이 충돌했는지 확인
                if player_y + 50 <= obstacle["y"] + 10:   # 플레이어가 장애물을 밟았으면
                    obstacle["x"] = WIDTH + random.randint(100, 300)   # 장애물을 새로운 위치로 이동
                    score += 10  # 점수 추가
                else:  # 충돌 시 게임 오버
                    game_over_sound.play()
                    game_state = "game_over"

        for coin in coins:
            coin_rect = pygame.Rect(coin["x"], coin["y"], 30, 30)
            if player_rect.colliderect(coin_rect):
                coin["x"] = WIDTH + random.randint(500, 800)
                score += 10
# 보스 상태 활성화
        if score >= 400 and not boss_active:  # 점수가 400 이상이면 보스 활성화
            boss_active = True

        if boss_active:  # 보스가 활성화되었을 때 보스 움직임 및 공격 패턴
            boss_x += boss_direction * boss_speed  # 보스 이동
            if boss_x <= 50 or boss_x >= WIDTH - boss_image.get_width() - 50:  # 화면 경계 확인
                boss_direction *= -1  # 방향 반전

            boss_attack_timer += 1
            if boss_attack_timer >= 180:  # 공격 주기
                ice_beams.append({"x": boss_x + boss_image.get_width() // 2 - 20, "y": boss_y + 70})  # 얼음빔 생성
                boss_attack_timer = 0  # 타이머 리셋

            for beam in ice_beams:
                beam["x"] -= 7
                if player_rect.colliderect(pygame.Rect(beam["x"], beam["y"], 40, 20)):
                    ice_beams.remove()
                    is_disabled = True
                    disable_timer = FPS * 2
                elif beam["x"] < 0:
                    ice_beams.remove()

            boss_rect = pygame.Rect(boss_x, boss_y, boss_image.get_width(), boss_image.get_height())
        # 보스와 플레이어 충돌 및 게임 클리어 조건
            if player_rect.colliderect(boss_rect):  # 플레이어와 보스 충돌 검사
                if player_y + 50 <= boss_y + 10:  # 플레이어가 보스를 밟았을 때
                    boss_health -= 1  # 보스 체력 감소
                    resize_boss()  # 보스 크기 축소
                    player_velocity_y = player_jump  # 플레이어 점프
                    if boss_health <= 0:  # 보스 체력이 0이 되면 게임 클리어
                        score += 1000
                        game_state = "game_clear"
                else:  # 보스와 일반 충돌
                    game_over_sound.play()
                    game_state = "game_over"

            screen.blit(boss_image, (boss_x, boss_y))
            for beam in ice_beams:
                screen.blit(ice_beam_image, (beam["x"], beam["y"]))

        if is_disabled:
            disable_timer -= 1
            if disable_timer <= 0:
                is_disabled = False

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(player_image, (player_x, player_y))
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle["x"], obstacle["y"]))
        for coin in coins:
            screen.blit(coin_image, (coin["x"], coin["y"]))

    elif game_state == "paused":
        paused_text = font.render("Game Paused - Press Esc to Resume", True, BLACK)
        screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, HEIGHT // 2))

    elif game_state == "game_clear":
        if not pygame.mixer.get_busy():
            game_clear_sound.play()
        screen.blit(game_clear_image, (0,0))
        game_clear_text = font.render("GAME CLEAR!!", True, BLACK)
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(game_clear_text, (WIDTH // 2 - game_clear_text.get_width() // 2, HEIGHT // 3))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 3 + 40))

    elif game_state == "game_over":
        screen.blit(game_over_image, (0,0))
        game_over_text = font.render("GAME OVER - Press Enter to Restart or ESC to Quit", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 3))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
