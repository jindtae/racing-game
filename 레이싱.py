import pygame
import random

# 파이게임 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

# 프레임 속도 조절을 위한 시계
clock = pygame.time.Clock()
FPS = 60

# 플레이어 자동차 크기
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

# 적 자동차 크기
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 100

# 폰트 초기화
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    # 화면에 텍스트 렌더링 및 그리기
    screen.blit(font.render(text, True, color), (x, y))

class PlayerCar:
    def __init__(self):
        # 플레이어 자동차 초기 위치 설정 (화면 아래쪽 중앙)
        self.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = BLUE
        self.speed = 5
        print("플레이어 자동차 초기화 위치:", self.x, self.y)

    def draw(self):
        # 플레이어 자동차를 사각형으로 그리기
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        # 사용자 입력에 따라 왼쪽 또는 오른쪽으로 이동
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            print("플레이어 자동차 왼쪽 이동:", self.x)
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            print("플레이어 자동차 오른쪽 이동:", self.x)

class EnemyCar:
    def __init__(self, number):
        # 적 자동차 초기 위치와 속도 설정
        self.x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
        self.y = -ENEMY_HEIGHT
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.color = random.choice([RED, GREEN, YELLOW, ORANGE, PURPLE, CYAN])
        self.speed = random.randint(3, 7)
        self.number = chr(64 + number)  # 번호를 알파벳으로 변환
        print("적 자동차 초기화 위치:", self.x, self.y, "속도:", self.speed, "색상:", self.color)

    def draw(self):
        # 적 자동차를 사각형으로 그리기
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # 적 자동차에 알파벳 표시
        draw_text(str(self.number), BLACK, self.x + self.width // 2 - 10, self.y + self.height // 2 - 10)

    def move(self):
        # 적 자동차를 아래로 이동
        self.y += self.speed
        print("적 자동차 이동 위치:", self.x, self.y)

        # 적 자동차가 화면 아래로 나가면 위치를 리셋
        if self.y > SCREEN_HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.speed = random.randint(3, 7)
            self.color = random.choice([RED, GREEN, YELLOW, ORANGE, PURPLE, CYAN])
            print("적 자동차 리셋 위치:", self.x, self.y, "새 속도:", self.speed, "새 색상:", self.color)

def main():
    # 메인 게임 루프
    run = True
    player = PlayerCar()  # 플레이어 자동차 초기화
    enemies = [EnemyCar(i + 1) for i in range(7)]  # 적 자동차 목록 생성
    score = 1  # 점수 시작 값을 1로 설정
    next_enemy_to_hit = 'A'  # 충돌해야 할 다음 적 자동차의 알파벳

    while run:
        clock.tick(FPS)  # 프레임 속도 조절
        screen.fill(WHITE)  # 화면 초기화

        # 플레이어 자동차 그리기
        player.draw()

        # 적 자동차 이동 및 그리기
        for enemy in enemies[:]:  # 적 자동차 목록 복사하여 반복
            enemy.move()
            enemy.draw()

            # 플레이어와 적 자동차 간 충돌 감지 (사각형 충돌 처리)
            if (player.x < enemy.x + enemy.width and
                player.x + player.width > enemy.x and
                player.y < enemy.y + enemy.height and
                player.y + player.height > enemy.y):
                if enemy.number == next_enemy_to_hit:
                    print(f"충돌 감지! 적 자동차 {enemy.number} 제거.")
                    enemies.remove(enemy)  # 충돌한 적 자동차 제거
                    next_enemy_to_hit = chr(ord(next_enemy_to_hit) + 1)  # 다음 적 자동차 알파벳으로 이동
                else:
                    print(f"게임 오버! {enemy.number}번은 아직 충돌할 차례가 아닙니다.")
                    run = False  # 게임 종료

        # 화면에 점수 표시
        draw_text(f"Score: {score}", BLACK, 10, 10)
        draw_text(f"Next: {next_enemy_to_hit}", BLACK, 10, 40)

        # 점수 업데이트
        score += 1
        if score >= 5000:  # 3분 (180초) 게임 오버 조건
            print("게임 오버! 제한 시간 초과.")
            run = False

        print("현재 점수:", score)

        # 사용자 입력 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 종료 이벤트 확인
                print("게임 종료 이벤트 감지. 종료합니다.")
                run = False

        # 키 입력에 따라 플레이어 자동차 이동
        keys = pygame.key.get_pressed()
        player.move(keys)

        pygame.display.update()  # 화면 업데이트

    pygame.quit()  # 파이게임 종료
    print("게임 루프 종료. Pygame 종료.")

if __name__ == "__main__":
    main()
