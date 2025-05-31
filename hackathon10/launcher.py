import pygame
import sys
import random
import minigame

# minigame 모듈이 없을 때 임시로 작동할 advance_time 정의
try:
    import minigame
except ImportError:
    def advance_time():
        print("[Warning] minigame 모듈을 찾을 수 없어 기본 시간 경과 동작 실행")
        # 기본적으로 변화 없음
        return 0, 0, 0

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 32
MAP_WIDTH, MAP_HEIGHT = 40, 30  # 맵 크기 (타일 수)
CHAR_SCALE = 0.08
BUILD_SCALE = 0.14
MAP_SCALE = 1.2  # 맵 및 배경 확대 배율

# 선택창 썸네일 관련
THUMB_SIZE = 200
H_SPACING = 50
V_SPACING = 15

# 기본 스탯 값
INITIAL_HEALTH = 100
INITIAL_MONEY = 1000
INITIAL_GPA = 0.0
INITIAL_YEAR = 1
INITIAL_SEM = 1
INITIAL_MONTH = 3
CREDITS_PER_SEM_START = 8

CHAR_NAMES = ["[공대생]", "[인문대생]", "[체대생]"]
CHAR_DESC = [
    "논리적 사고와 문제 해결에 강함. 체력↓ 졸업학점↑ 자본↑",
    "글쓰기와 인문적 통찰이 뛰어남. 체력↓ 졸업학점↓",
    "신체 능력이 뛰어나며 팀워크를 중시함. 체력↑"
]
CHAR_IMAGE_FILES = [
    [f"engineer_{i}.png" for i in range(3)],
    [f"humanities_{i}.png" for i in range(3)],
    [f"sports_{i}.png" for i in range(3)]
]

BUILDINGS = [
    ("main", "본관", (20, 14)), #
    ("hall", "공식당", (17, 22)), #
    ("social", "사과대", (30, 18)), #
    ("field", "운동장", (9, 25)), #
    ("dorm", "기숙사", (28, 4)), #
    ("library", "도서관", (22, 8)),#
    ("it", "IT대학", (12, 14)) #
]

# 디버그 팝업 크기 및 버튼 크기
POPUP_WIDTH, POPUP_HEIGHT = 400, 350
BUTTON_SIZE = 24
BUTTON_MARGIN = 20
STAT_LINE_HEIGHT = 30
TOGGLE_BTN_WIDTH, TOGGLE_BTN_HEIGHT = 100, 30

class Game:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("malgungothic", 20)
        self.state = 'MENU'
        self.selected_char = 0
        self.debug = False
        self.show_grid = False
        # 초기 스탯 값
        self.health = INITIAL_HEALTH
        self.money = INITIAL_MONEY
        self.gpa = INITIAL_GPA
        self.year = INITIAL_YEAR
        self.semester = INITIAL_SEM
        self.month = INITIAL_MONTH
        self.credits_required = CREDITS_PER_SEM_START
        self.credits_earned = 0

        # 배경 이미지 변수들 초기화
        self.bg_menu = None
        self.bg_select = None
        self.bg_play = None

        self.load_assets()

    def load_assets(self):
        # 로고 이미지 불러오기, smoothscale 사용하여 픽셀 깨짐 방지
        try:
            self.logo = pygame.image.load("logo.png").convert_alpha()
            lw, lh = self.logo.get_size()
            logo_width = 290
            logo_height = int(lh * (logo_width / lw))
            self.logo = pygame.transform.smoothscale(self.logo, (logo_width, logo_height))
            pygame.display.set_icon(self.logo)
        except Exception as e:
            print(f"[Warning] logo.png 로드 실패: {e}")
            self.logo = None

        # 배경 이미지 로드 시도
        try:
            bg0 = pygame.image.load("background_0.png").convert()
            self.bg_menu = pygame.transform.smoothscale(bg0, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"[Warning] background_0.png 로드 실패: {e}")
            self.bg_menu = None

        try:
            bg1 = pygame.image.load("background_1.png").convert()
            self.bg_select = pygame.transform.smoothscale(bg1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"[Warning] background_1.png 로드 실패: {e}")
            self.bg_select = None

        try:
            # background_2.png를 맵 전체 크기에 맞춰 불러온 후, MAP_SCALE로 확대합니다.
            bg2 = pygame.image.load("background_2.png").convert()
            map_pixel_w = int(MAP_WIDTH * TILE_SIZE * MAP_SCALE)
            map_pixel_h = int(MAP_HEIGHT * TILE_SIZE * MAP_SCALE)
            self.bg_play = pygame.transform.smoothscale(bg2, (map_pixel_w, map_pixel_h))
        except Exception as e:
            print(f"[Warning] background_2.png 로드 실패: {e}")
            self.bg_play = None

        # 캐릭터 이미지
        self.raw_char_images = []
        for files in CHAR_IMAGE_FILES:
            loaded_frames = []
            for f in files:
                try:
                    loaded_frames.append(pygame.image.load(f).convert_alpha())
                except Exception as e:
                    print(f"[Warning] 캐릭터 이미지 {f} 로드 실패: {e}")
                    # 빈 서피스라도 있어야 인덱스 에러 방지
                    loaded_frames.append(pygame.Surface((64, 64), pygame.SRCALPHA))
            self.raw_char_images.append(loaded_frames)

        # 게임 내 캐릭터 크기 적용
        self.char_images = []
        for frames in self.raw_char_images:
            scaled = []
            for img in frames:
                w, h = img.get_size()
                sw, sh = int(w * CHAR_SCALE), int(h * CHAR_SCALE)
                if sw <= 0: sw = 1
                if sh <= 0: sh = 1
                scaled.append(pygame.transform.smoothscale(img, (sw, sh)))
            self.char_images.append(scaled)

        # 건물 이미지
        self.building_images = {}
        for key, name, _ in BUILDINGS:
            try:
                img = pygame.image.load(f"{key}.png").convert_alpha()
                w, h = img.get_size()
                bw, bh = int(w * BUILD_SCALE), int(h * BUILD_SCALE)
                if bw <= 0: bw = 1
                if bh <= 0: bh = 1
                self.building_images[key] = pygame.transform.smoothscale(img, (bw, bh))
            except Exception as e:
                print(f"[Warning] 건물 이미지 {key}.png 로드 실패: {e}")
                # 대신 색칠된 사각형(placeholder) 생성
                placeholder = pygame.Surface((int(TILE_SIZE * BUILD_SCALE * 2), int(TILE_SIZE * BUILD_SCALE * 2)), pygame.SRCALPHA)
                placeholder.fill((180, 180, 180))
                self.building_images[key] = placeholder

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines, current = [], ''
        for w in words:
            test = current + (' ' if current else '') + w
            if self.font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    def draw_text_center(self, text, x, y):
        surf = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surf, (x - surf.get_width() // 2, y))

    def draw_text_right(self, text, right_x, y):
        surf = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(surf, (right_x - surf.get_width(), y))

    def normalize_time(self):
        # 월/학기/학년 정규화
        if self.month < 1:
            while self.month < 1:
                self.month += 12; self.semester -= 1
        if self.month > 12:
            while self.month > 12:
                self.month -= 12; self.semester += 1
        if self.semester < 1:
            while self.semester < 1:
                self.semester += 2; self.year -= 1
        if self.semester > 2:
            while self.semester > 2:
                self.semester -= 2; self.year += 1
        if self.year < 1:
            self.year = 1

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.debug = not self.debug
                if self.state == 'MENU' and event.key == pygame.K_SPACE:
                    self.state = 'SELECT'
                elif self.state == 'SELECT':
                    if event.key == pygame.K_LEFT:
                        self.selected_char = (self.selected_char - 1) % len(self.char_images)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_char = (self.selected_char + 1) % len(self.char_images)
                    elif event.key == pygame.K_RETURN:
                        self.init_play()
                        self.state = 'PLAY'
            if event.type == pygame.MOUSEBUTTONDOWN and self.debug:
                self.handle_debug_click(event.pos)

    def update(self):
        if self.state == 'PLAY':
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 4
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 4
            self.player.move(dx, dy)
            self.player.update_animation(dx, dy)
            px = self.player.x + self.player.width // 2
            py = self.player.y + self.player.height // 2
            self.near_building = None
            for key, name, (gx, gy) in BUILDINGS:
                bx = gx * TILE_SIZE + TILE_SIZE // 2; by = gy * TILE_SIZE + TILE_SIZE // 2
                if ((px - bx)**2 + (py - by)**2)**0.5 <= TILE_SIZE:
                    self.near_building = name
                    break
            if keys[pygame.K_SPACE] and self.near_building:
                self.advance_game_time(self.near_building)
                
                

    def init_play(self):
        self.player = Player(self.char_images[self.selected_char])
        self.player.x = SCREEN_WIDTH // 2 - self.player.width // 2
        self.player.y = SCREEN_HEIGHT // 2 - self.player.height // 2

    def advance_game_time(self, near_building):
        # minigame.advance_time가 (체력 변량, 돈 변량, 학점 변량)을 반환한다고 가정
        if near_building == "본관":dh, dm, dc = minigame.minigame.eta_review_minigame() ##########################################
        elif near_building == "기숙사": dh, dm, dc = minigame.minigame.play_course_battle()
        elif  near_building == "운동장": dh, dm, dc = minigame.minigame.track_race_event()
        elif  near_building == "도서관": dh, dm, dc = minigame.minigame.professor_begging_email()
        elif  near_building == "공식당":
            dh, dm, dc = minigame.minigame.run_mt_game()
            # pygame.display.set_mode((800, 800))
        elif  near_building == "사과대대": dh, dm, dc = minigame.minigame.run_class_late_event()
        else: dh, dm, dc = 0, 0, 0

        pygame.display.set_caption("졸업까지 1만시간")

        # 반환 값 반영
        self.health += dh
        self.money += dm
        self.credits_earned += dc
        # 시간 흐름 로직
        self.month += 1
        self.normalize_time()
        # 방학 이벤트 조건 재확인 (추가 변화 없음)
        if self.month in (7, 12):
            pass  # minigame에서 처리했으므로 별도 처리 생략
        # 학기/학년 학점 부족/졸업 처리
        if self.semester == 1 and self.month == 3 and self.credits_earned < self.credits_required:
            self.end_game(False, "학점 부족")
        if self.year > 4:
            self.end_game(True)

    def end_game(self, win, reason=None):
        print("졸업" if win else f"게임오버: {reason}")
        self.__init__(self.screen)

    def handle_debug_click(self, pos):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        stats = ["health", "money", "gpa", "year", "semester", "month", "credits_earned", "credits_required"]
        for i, stat in enumerate(stats):
            line_y = popup_y + 30 + i * STAT_LINE_HEIGHT
            minus_x = popup_x + BUTTON_MARGIN
            plus_x = popup_x + POPUP_WIDTH - BUTTON_MARGIN - BUTTON_SIZE
            minus_rect = pygame.Rect(minus_x, line_y - BUTTON_SIZE // 2, BUTTON_SIZE, BUTTON_SIZE)
            plus_rect = pygame.Rect(plus_x, line_y - BUTTON_SIZE // 2, BUTTON_SIZE, BUTTON_SIZE)
            if minus_rect.collidepoint(pos):
                setattr(self, stat, getattr(self, stat) - (1 if stat != 'gpa' else 0.1))
                if stat in ['month', 'semester']:
                    self.normalize_time()
                    if self.month in (7, 12):
                        dh, dm = random.randint(5, 15), random.randint(50, 200)
                        self.health += dh; self.money += dm
            elif plus_rect.collidepoint(pos):
                setattr(self, stat, getattr(self, stat) + (1 if stat != 'gpa' else 0.1))
                if stat in ['month', 'semester']:
                    self.normalize_time()
                    if self.month in (7, 12):
                        dh, dm = random.randint(5, 15), random.randint(50, 200)
                        self.health += dh; self.money += dm

        # Toggle Grid 버튼 영역 검사
        toggle_x = popup_x + (POPUP_WIDTH - TOGGLE_BTN_WIDTH) // 2
        toggle_y = popup_y + POPUP_HEIGHT - BUTTON_MARGIN - TOGGLE_BTN_HEIGHT
        toggle_rect = pygame.Rect(toggle_x, toggle_y, TOGGLE_BTN_WIDTH, TOGGLE_BTN_HEIGHT)
        if toggle_rect.collidepoint(pos):
            self.show_grid = not self.show_grid

    def draw(self):
        # --------------------------------------------------------------------
        # 1) MENU 화면: background_0.png 또는 대체 색깔로 채우기
        # --------------------------------------------------------------------
        if self.state == 'MENU':
            if self.bg_menu:
                self.screen.blit(self.bg_menu, (0, 0))
            else:
                # 못 불러왔을 때 연한 회색으로 채움
                self.screen.fill((180, 180, 180))
            # 로고 표시
            if self.logo:
                lw, lh = self.logo.get_size()
                self.screen.blit(self.logo, (SCREEN_WIDTH//2 - lw//2, SCREEN_HEIGHT//2 - lh - 20))
            # 시작 텍스트
            self.draw_text_center("[스페이스] 시작", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)

        # --------------------------------------------------------------------
        # 2) SELECT 화면: background_1.png 또는 대체 색깔로 채우기
        # --------------------------------------------------------------------
        elif self.state == 'SELECT':
            if self.bg_select:
                self.screen.blit(self.bg_select, (0, 0))
            else:
                # 못 불러왔을 때 연한 파란색으로 채움
                self.screen.fill((200, 220, 255))

            # 캐릭터 선택 UI
            self.draw_select()

        # --------------------------------------------------------------------
        # 3) PLAY 화면: 확대된 background_2.png + 확대된 맵 + 회색 바깥 부분 + HUD
        # --------------------------------------------------------------------
        elif self.state == 'PLAY':
            # 화면 전체 회색으로 먼저 채워서 맵 바깥 영역 회색 처리
            self.screen.fill((100, 100, 100))

            # 배경 그리기 (맵에 고정, 스크롤 및 확대 적용)
            if self.bg_play:
                # 플레이어 좌표에 MAP_SCALE을 곱해서 스크롤 오프셋 계산
                offset_x = int(self.player.x * MAP_SCALE - SCREEN_WIDTH // 2 + (self.player.width * MAP_SCALE) // 2)
                offset_y = int(self.player.y * MAP_SCALE - SCREEN_HEIGHT // 2 + (self.player.height * MAP_SCALE) // 2)
                bg_x = -offset_x
                bg_y = -offset_y
                self.screen.blit(self.bg_play, (bg_x, bg_y))
            else:
                # 배경 이미지 없을 때
                self.screen.fill((200, 220, 255))

            # 타일 그리기 (show_grid가 True일 때만)
            if self.show_grid:
                for gx in range(MAP_WIDTH):
                    for gy in range(MAP_HEIGHT):
                        bx = int(gx * TILE_SIZE * MAP_SCALE - offset_x)
                        by = int(gy * TILE_SIZE * MAP_SCALE - offset_y)
                        tile_size_scaled = int(TILE_SIZE * MAP_SCALE)
                        pygame.draw.rect(self.screen, (180, 200, 230), (bx, by, tile_size_scaled, tile_size_scaled), 1)

            # 빌딩 그리기 (확대 적용)
            for key, _, (gx, gy) in BUILDINGS:
                base_img = self.building_images[key]
                # BUILD_SCALE 후, MAP_SCALE을 추가로 적용하여 크기 조정
                build_img = pygame.transform.rotozoom(base_img, 0, MAP_SCALE)
                bw, bh = build_img.get_size()
                center_x = gx * TILE_SIZE * MAP_SCALE + (TILE_SIZE * MAP_SCALE) / 2
                center_y = gy * TILE_SIZE * MAP_SCALE + (TILE_SIZE * MAP_SCALE) / 2
                bx = int(center_x - bw / 2 - offset_x)
                by = int(center_y - bh / 2 - offset_y)
                self.screen.blit(build_img, (bx, by))

            # 플레이어 그리기 (화면 중앙 고정, 확대 적용)
            frame = self.player.frames[self.player.idx]
            frame_scaled = pygame.transform.rotozoom(frame, 0, MAP_SCALE)
            pw_scaled, ph_scaled = frame_scaled.get_size()
            px = SCREEN_WIDTH // 2 - pw_scaled // 2
            py = SCREEN_HEIGHT // 2 - ph_scaled // 2
            self.screen.blit(frame_scaled, (px, py))

            # 상호작용 가능한 건물이 가까이 있으면 안내
            if getattr(self, 'near_building', None):
                self.draw_text_center("[스페이스] 상호작용 가능", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)

            # HUD (체력, 돈, 학점, 시간)
            self.draw_hud()

            # 디버그 모드일 경우 팝업
            if self.debug:
                self.draw_debug_popup()

    def draw_select(self):
        self.draw_text_center("캐릭터 선택 (← → 엔터)", SCREEN_WIDTH // 2, 40)
        total_w = len(self.char_images) * THUMB_SIZE + (len(self.char_images) - 1) * H_SPACING
        start_x = SCREEN_WIDTH // 2 - total_w // 2
        y = 100
        for i, frames in enumerate(self.char_images):
            x = start_x + i * (THUMB_SIZE + H_SPACING)
            thumb = pygame.transform.scale(self.raw_char_images[i][0], (THUMB_SIZE, THUMB_SIZE))
            self.screen.blit(thumb, (x, y))
            if i == self.selected_char:
                pygame.draw.rect(self.screen, (255, 255, 0), (x, y, THUMB_SIZE, THUMB_SIZE), 3)
            name_y = y + THUMB_SIZE + V_SPACING
            self.draw_text_center(CHAR_NAMES[i], x + THUMB_SIZE // 2, name_y)
            desc_y = name_y + V_SPACING + 4
            for idx, line in enumerate(self.wrap_text(CHAR_DESC[i], THUMB_SIZE)):
                self.draw_text_center(line, x + THUMB_SIZE // 2, desc_y + idx * (self.font.get_height() + 2))

    def draw_hud(self):
        right_x = SCREEN_WIDTH - 10
        y0 = 20
        stats = [
            f"체력: {self.health}",
            f"돈: {self.money}",
            f"학점: {self.credits_earned}/{self.credits_required}",
            f"시간: {self.year}년 {self.semester}학기 {self.month}월"
        ]
        for i, s in enumerate(stats):
            self.draw_text_right(s, right_x, y0 + i * 24)

    def draw_debug_popup(self):
        popup_x = (SCREEN_WIDTH - POPUP_WIDTH) // 2
        popup_y = (SCREEN_HEIGHT - POPUP_HEIGHT) // 2
        pygame.draw.rect(self.screen, (240, 240, 240), (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT))
        pygame.draw.rect(self.screen, (0, 0, 0), (popup_x, popup_y, POPUP_WIDTH, POPUP_HEIGHT), 2)
        self.draw_text_center("디버그", popup_x + POPUP_WIDTH // 2, popup_y + 10)
        stats = [("체력", self.health), ("돈", self.money), ("GPA", round(self.gpa, 2)),
                 ("학년", self.year), ("학기", self.semester), ("월", self.month),
                 ("이수학점", self.credits_earned), ("필요학점", self.credits_required)]
        for i, (label, value) in enumerate(stats):
            y = popup_y + 30 + i * STAT_LINE_HEIGHT
            label_text = f"{label}: {value}"
            label_surf = self.font.render(label_text, True, (0, 0, 0))
            center_x = popup_x + POPUP_WIDTH // 2
            label_x = center_x - label_surf.get_width() // 2
            self.screen.blit(label_surf, (label_x, y))

            minus_rect = pygame.Rect(popup_x + BUTTON_MARGIN, y - BUTTON_SIZE // 2, BUTTON_SIZE, BUTTON_SIZE)
            pygame.draw.rect(self.screen, (200, 0, 0), minus_rect)
            self.draw_text_center("-", minus_rect.centerx, minus_rect.centery)

            plus_rect = pygame.Rect(popup_x + POPUP_WIDTH - BUTTON_MARGIN - BUTTON_SIZE,
                                    y - BUTTON_SIZE // 2, BUTTON_SIZE, BUTTON_SIZE)
            pygame.draw.rect(self.screen, (0, 200, 0), plus_rect)
            self.draw_text_center("+", plus_rect.centerx, plus_rect.centery)

        # Grid 토글 버튼
        toggle_x = popup_x + (POPUP_WIDTH - TOGGLE_BTN_WIDTH) // 2
        toggle_y = popup_y + POPUP_HEIGHT - BUTTON_MARGIN - TOGGLE_BTN_HEIGHT
        toggle_rect = pygame.Rect(toggle_x, toggle_y, TOGGLE_BTN_WIDTH, TOGGLE_BTN_HEIGHT)
        pygame.draw.rect(self.screen, (100, 100, 100), toggle_rect)
        txt = "그리드: 켜짐" if self.show_grid else "그리드: 꺼짐"
        self.draw_text_center(txt, toggle_x + TOGGLE_BTN_WIDTH // 2, toggle_y + (TOGGLE_BTN_HEIGHT - self.font.get_height()) // 2)

class Player:
    def __init__(self, frames):
        self.frames = frames
        self.idx = 0
        self.timer = 0
        self.delay = 12
        self.width, self.height = frames[0].get_size()
        self.x = 0
        self.y = 0
        self.moving = False

    def update_animation(self, dx, dy):
        self.moving = dx != 0 or dy != 0
        if self.moving:
            self.timer += 1
            if self.timer >= self.delay:
                self.idx = (self.idx + 1) % len(self.frames)
                self.timer = 0
        else:
            self.idx = 0
            self.timer = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        max_x = MAP_WIDTH * TILE_SIZE - self.width
        max_y = MAP_HEIGHT * TILE_SIZE - self.height
        self.x = max(0, min(new_x, max_x))
        self.y = max(0, min(new_y, max_y))

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("졸업까지 1만시간")
    # pygame.display.set_mode((800, 800))
    Game(screen).run()
