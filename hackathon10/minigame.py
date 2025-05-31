import pygame
import sys
import random
import time
import os

class minigame:
    @staticmethod
    def run_class_late_event():
        pygame.init()
        screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("지각 방지 달리기")
        font = pygame.font.SysFont("malgungothic", 24)
        timer_font = pygame.font.SysFont("malgungothic", 32, bold=True)

        player_x = 50
        player_y = 180
        player_speed = 5
        track_length = 700

        last_key = None
        clock = pygame.time.Clock()
        start_time = None
        game_started = False
        result = None

        running = True
        while running:
            screen.fill((200, 230, 255))  # 배경

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not game_started:
                screen.fill((255, 255, 255))
                screen.blit(font.render("🏃 수업 지각 방지 미니게임!", True, (0, 0, 0)), (240, 100))
                screen.blit(font.render("6초 안에 도착하지 못하면 지각입니다!", True, (0, 0, 0)), (240, 140))
                screen.blit(font.render("A와 D 키를 번갈아 눌러서 달려가세요!", True, (0, 0, 0)), (240, 180))
                screen.blit(font.render("ENTER 키를 눌러 시작", True, (150, 0, 0)), (240, 240))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        start_time = time.time()
                        game_started = True
                continue

            # 조작 처리
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and last_key != 'a':
                player_x += player_speed
                last_key = 'a'
            elif keys[pygame.K_d] and last_key != 'd':
                player_x += player_speed
                last_key = 'd'

            # 트랙 및 캐릭터
            pygame.draw.line(screen, (255, 255, 255), (0, 150), (800, 150), 4)
            pygame.draw.line(screen, (255, 255, 255), (0, 230), (800, 230), 4)
            pygame.draw.line(screen, (255, 215, 0), (track_length, 140), (track_length, 240), 6)
            pygame.draw.rect(screen, (30, 144, 255), (player_x, player_y, 30, 30))

            # 타이머 표시
            elapsed = time.time() - start_time
            remain = max(0, 6.0 - elapsed)
            timer_surface = timer_font.render(f"남은 시간: {remain:.1f}초", True, (200, 0, 0))
            screen.blit(timer_surface, (400 - timer_surface.get_width() // 2, 20))

            # 게임 결과 판정
            if player_x >= track_length and result is None:
                result = "success"
                result_time = time.time()
            elif elapsed >= 6 and result is None:
                result = "fail"
                result_time = time.time()

            # 결과 메시지
            if result is not None:
                if result == "success":
                    msg = "성공! 수업에 제시간에 도착했습니다. 학점 +1"
                    color = (0, 128, 0)
                else:
                    msg = "실패... 지각했습니다. 학점 -1"
                    color = (200, 0, 0)
                result_text = font.render(msg, True, color)
                screen.blit(result_text, (180, 300))

                if time.time() - result_time > 2:
                    if result == "success":
                        return 0, 0, 1
                    else:
                        return 0, 0, -1

            pygame.display.flip()
            clock.tick(60)

    @staticmethod
    def eta_review_minigame():
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("에타 강의 평가 맞추기")
        font = pygame.font.SysFont("malgungothic", 24)
        large_font = pygame.font.SysFont("malgungothic", 32, bold=True)

        total_reviews = [
            {"text": "교수님 말 진짜 빠름, 이해 안 됨", "correct": 2.3, "options": [2.3, 3.5, 4.1]},
            {"text": "팀플 없음. 과제만 하면 A+ 줌", "correct": 4.8, "options": [4.8, 3.2, 2.5]},
            {"text": "출석 하나도 안 보심. 시험은 빡셈", "correct": 3.1, "options": [2.1, 3.1, 4.5]},
            {"text": "과제도 많고 시험도 어려운데 이상하게 듣고 싶음", "correct": 4.2, "options": [4.2, 3.8, 2.9]},
            {"text": "진도 너무 느림. 졸려요...", "correct": 2.7, "options": [2.7, 3.0, 4.3]},
            {"text": "이해는 잘 되는데 시험이 과하게 어려움", "correct": 3.4, "options": [3.4, 4.6, 2.9]},
            {"text": "교수님 유머감각 쩔어요. 재밌어요.", "correct": 4.9, "options": [4.9, 3.8, 2.6]},
            {"text": "PPT만 읽고 끝냄. 비추.", "correct": 2.0, "options": [2.0, 3.0, 4.0]},
            {"text": "질문 잘 받음. 조교도 친절함", "correct": 4.5, "options": [4.5, 3.3, 2.5]},
            {"text": "과제 많지만 배울 게 많음", "correct": 4.1, "options": [4.1, 3.6, 2.2]},
            {"text": "기말고사 비중 80% 주의", "correct": 3.0, "options": [3.0, 2.2, 4.0]},
            {"text": "시험문제 예상 가능해서 무난함", "correct": 4.0, "options": [4.0, 3.1, 2.0]},
            {"text": "교수님 피드백 없음. 혼자 공부해야 함", "correct": 2.5, "options": [2.5, 3.7, 4.4]},
            {"text": "슬라이드 깔끔, 설명 이해 쉬움", "correct": 4.6, "options": [4.6, 3.3, 2.4]},
            {"text": "사바사 강의. 조별과제 조심", "correct": 3.3, "options": [3.3, 2.9, 4.7]},
        ]

        reviews = random.sample(total_reviews, 5)
        current_idx = 0
        selected = -1
        result = None
        correct_count = 0

        running = True
        while running:
            screen.fill((235, 245, 255))
            current = reviews[current_idx]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if result is None:
                        if event.key in [pygame.K_1, pygame.K_KP1]: selected = 0
                        elif event.key in [pygame.K_2, pygame.K_KP2]: selected = 1
                        elif event.key in [pygame.K_3, pygame.K_KP3]: selected = 2
                        if selected != -1:
                            guess = current["options"][selected]
                            result = (guess == current["correct"])
                            if result:
                                correct_count += 1
                    else:
                        if event.key == pygame.K_RETURN:
                            current_idx += 1
                            selected = -1
                            result = None
                            if current_idx >= len(reviews):
                                running = False

            pygame.draw.rect(screen, (255, 255, 255), (40, 40, 720, 500), border_radius=10)
            pygame.draw.rect(screen, (100, 100, 200), (40, 40, 720, 500), 3, border_radius=10)

            title = large_font.render(f"문제 {current_idx+1} / 5", True, (20, 20, 80))
            screen.blit(title, (400 - title.get_width()//2, 60))

            text_label = font.render("강의평:", True, (0,0,0))
            screen.blit(text_label, (80, 120))
            t = font.render(current["text"], True, (0,0,0))
            screen.blit(t, (100, 160))

            base_y = 240
            for i, opt in enumerate(current["options"]):
                label = f"{i+1}. 평점: {opt}"
                color = (0,0,255) if selected == i else (30,30,30)
                t = font.render(label, True, color)
                pygame.draw.rect(screen, (200,200,255), (80, base_y + i*50, 300, 40), border_radius=5)
                screen.blit(t, (100, base_y + 10 + i*50))

            if result is not None:
                msg = "정답입니다! 학점 +1 :)" if result else "오답입니다... 체력 -10"
                t = font.render(msg, True, (255,0,0) if not result else (0,128,0))
                screen.blit(t, (80, 430))
                sub = font.render("[ENTER] 다음 문제", True, (80,80,80))
                screen.blit(sub, (80, 460))

            pygame.display.flip()

        pygame.time.delay(100)
        #pygame.quit()

        hp_change = (5 - correct_count) * -10
        gpa_change = correct_count
        return hp_change, 0, gpa_change ######################### (체력 변량, 돈 변량, 학점 변량)

    @staticmethod
    def play_course_battle():
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("수강신청 배틀로얄")
        font = pygame.font.SysFont("malgungothic", 28)

        subjects = ["데이터구조", "철학개론", "운동과 건강", "AI프로그래밍", "한국문학개론"]
        success_count = 0

        screen.fill((255,255,255))
        screen.blit(font.render("2인용 게임입니다. 친구를 데려오세요.", True, (0,0,0)), (100, 150))
        screen.blit(font.render("룰: A키 - 1P 수강신청 / L키 - 2P 방해", True, (0,0,0)), (100, 250))
        screen.blit(font.render("ENTER 키를 눌러 시작하세요", True, (0,0,200)), (100, 350))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

        for subject in subjects:
            screen.fill((255,255,255))
            screen.blit(font.render(f"[{subject}] 수강신청!", True, (0,0,0)), (100, 200))
            pygame.display.flip()

            responded = False
            while not responded:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            success_count += 1
                            responded = True
                        elif event.key == pygame.K_l:
                            responded = True
            pygame.time.delay(500)
        hp_change = -10 * (5 - success_count)
        gpa_change = success_count
        return hp_change, 0, gpa_change ######################### (체력 변량, 돈 변량, 학점 변량)

   
    @staticmethod
    def track_race_event():
        pygame.init()
        screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("대학 체육대회 - 달리기")
        font = pygame.font.SysFont("malgungothic", 24)

        # 주자 위치
        player_x = 50
        player_y = 90
        npc_x = [50, 50]
        npc_y = [170, 250]
        player_speed = 5
        npc_speed = [random.uniform(1.0, 2.0), random.uniform(1.5, 2.3)]
        track_length = 700

        last_key = None
        result = None
        clock = pygame.time.Clock()
        instructions = True
        show_result = False

        while True:
            screen.fill((0, 120, 0))  # 잔디 배경

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if instructions:
                screen.fill((255, 255, 255))
                info1 = font.render("🏃 체육대회 달리기 경기입니다!", True, (0, 0, 0))
                info2 = font.render("A키와 D키를 번갈아 눌러 달리세요!", True, (0, 0, 0))
                info3 = font.render("승리 시 돈 +10000원 / 패배 시 체력 -15", True, (0, 0, 0))
                info4 = font.render("Enter를 누르면 시작합니다.", True, (100, 0, 0))
                screen.blit(info1, (220, 100))
                screen.blit(info2, (220, 140))
                screen.blit(info3, (220, 180))
                screen.blit(info4, (220, 240))

                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        instructions = False
                continue

            # 트랙 선
            for y in [70, 150, 230, 310]:
                pygame.draw.line(screen, (255, 255, 255), (0, y), (800, y), 4)

            # 조작 처리
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and last_key != 'a':
                player_x += player_speed
                last_key = 'a'
            elif keys[pygame.K_d] and last_key != 'd':
                player_x += player_speed
                last_key = 'd'

            # NPC 자동 이동
            for i in range(len(npc_x)):
                npc_x[i] += npc_speed[i]

            # 결승선
            pygame.draw.line(screen, (255, 215, 0), (track_length, 60), (track_length, 320), 6)

            # 캐릭터들
            pygame.draw.rect(screen, (30, 144, 255), (player_x, player_y, 30, 30))  # 플레이어
            pygame.draw.rect(screen, (200, 200, 200), (npc_x[0], npc_y[0], 30, 30))  # NPC 1
            pygame.draw.rect(screen, (255, 99, 71), (npc_x[1], npc_y[1], 30, 30))    # NPC 2

            # 결과 판정
            if not show_result and (player_x >= track_length or max(npc_x) >= track_length):
                show_result = True
                if player_x >= track_length and all(n < track_length for n in npc_x):
                    result = "win"
                else:
                    result = "lose"
                result_time = time.time()

            if show_result:
                if result == "win":
                    msg = "승리! 돈 +10000원"
                else:
                    msg = "패배... 체력 -15"
                result_text = font.render(msg, True, (0, 128, 0) if result == "win" else (255, 0, 0))
                screen.blit(result_text, (280, 340))

                if time.time() - result_time > 2:
                    if result == "win":
                        return 0, 10000, 0 #체력 돈 학점
                    else:
                        return 15, 0, 0

            pygame.display.flip()
            clock.tick(60)

    @staticmethod
    def professor_begging_email():
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("교수님께 드리는 애원 메일")
        
        # ✔️ 한글 폰트 직접 지정
        font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 24)
        clock = pygame.time.Clock()

        # 랜덤 상황
        scenarios = [
            "외국인 교수님께 중간고사에 지각하여 재시험을 요청하는 상황.",
            "외국인 교수님께 수강 정원 초과 과목에 대해 수강 신청을 정정 요청하는 상황."
        ]
        situation = random.choice(scenarios)

        # 애절함 판단 키워드
        keywords = [
    "sorry", "apologize", "regret", "please", "request", "beg", "ask",
    "chance", "opportunity", "one more chance",
    "work hard", "study hard", "do my best", "sincerely",
    "really", "truly", "desperately", "earnestly",
    "situation", "reason", "emergency", "accident", "unavoidable",
    "beg you", "sincerely request", "desperately hope",
    "retake", "reschedule", "re-exam", "revise", "enrollment issue",
    "professor", "dear professor", "respected professor"
]

        input_text = ""
        result = None
        submitted = False
        show_result_timer = 0

        while True:
            screen.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not submitted:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            submitted = True
                            keyword_count = sum(1 for word in keywords if word in input_text)
                            if len(input_text) >= 100 and keyword_count >= 3:
                                result = "success"
                            else:
                                result = "fail"
                            show_result_timer = pygame.time.get_ticks()
                        else:
                            input_text += event.unicode

            # 제목 & 상황 표시
            title = font.render("📝 교수님께 메일을 작성하세요", True, (0, 0, 0))
            screen.blit(title, (40, 20))
            situation_text = font.render(f"상황: {situation}", True, (10, 10, 10))
            screen.blit(situation_text, (40, 60))

            # 입력창
            pygame.draw.rect(screen, (230, 230, 230), (40, 100, 720, 400))
            pygame.draw.rect(screen, (0, 0, 0), (40, 100, 720, 400), 2)

            # 줄바꿈 처리된 입력 텍스트
            words = input_text.split(' ')
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                if font.size(test_line)[0] < 700:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            lines.append(line)

            for i, l in enumerate(lines[-14:]):
                rendered = font.render(l.strip(), True, (0, 0, 0))
                screen.blit(rendered, (50, 110 + i * 28))

            if submitted:
                if result == "success":
                    msg = "음... 사정이 딱하니 이번만 봐주도록 하죠."
                    color = (0, 120, 0)
                else:
                    msg = "호호호 재수강하세요 학생~ (학점 -1)"
                    color = (200, 0, 0)
                res_text = font.render(msg, True, color)
                screen.blit(res_text, (40, 520))

                # 2초 후 종료
                if pygame.time.get_ticks() - show_result_timer > 4000:
                    if result == "success":
                        return (0, 0, +1)
                    else:
                        return (0, 0, -1)
            else:
                tip = font.render("※ 키보드로 입력 후 [ENTER]를 눌러 제출하세요", True, (100, 100, 100))
                screen.blit(tip, (40, 520))

            pygame.display.flip()
            clock.tick(30)

    @staticmethod
    def run_mt_game():
        import pygame
        import sys
        import time
        import random

        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("MT 주량 게임")
        font = pygame.font.Font("C:/Windows/Fonts/malgun.ttf", 24)
        clock = pygame.time.Clock()

        WHITE = (255, 255, 255)
        DARKGRAY = (100, 100, 100)
        RED = (200, 50, 50)
        GREEN = (50, 200, 50)
        BLACK = (0, 0, 0)

        last_auto_time = time.time()
        last_skip_time = -9999
        gauge = 0
        max_gauge = 10
        start_time = time.time()
        duration = 50  # 게임 시간 50초
        game_over = False

        skill_cooldowns = {1: 5, 2: 3, 3: 3}  # 화장실 가기 쿨타임을 3초로 줄임
        skill4_used = False
        last_skill_time = -9999

        hp_change = 0
        money_change = 0
        result_message = ""
        fm_message = ""
        debuff_message = ""
        debuff_time = 0
        skill_effect_message = ""
        skill_effect_time = 0

        def show_instructions():
            screen.fill(WHITE)
            lines = [
                "MT 주량 게임입니다! 50초 동안 주량을 조절하세요.",
                "1초마다 게이지가 0.5씩 오릅니다. 게이지 10 도달 시 게임오버!",
                "",
                "🛠 스킬 종류:",
                "1. 꺾어마시기 (게이지 증가 정지, 걸리면 체력 -3)",
                "2. 화장실 (게이지 -3, FM 확률 20%, 체력 -10)",
                "3. 몰래버리기 (게이지 -1, 걸리면 체력 -3, 게이지 +1)",
                "4. 숙취해소제 (게이지 초기화, 1회 한정)",
                "",
                "⚠️ 스킬은 [1][2][3][4] 키로 사용합니다.",
                "하나라도 쓰면 해당 쿨타임 동안 나머지 스킬도 잠깁니다.",
                "",
                "Enter를 눌러 시작하세요."
            ]
            for i, line in enumerate(lines):
                txt = font.render(line, True, BLACK)
                screen.blit(txt, (40, 30 + i * 28))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False

        show_instructions()

        while True:
            now = time.time()
            elapsed = now - start_time
            screen.fill(WHITE)

            if elapsed >= duration or game_over:
                result_lines = [
                    f"체력 변화: {hp_change}",
                    f"돈 변화: {money_change}",
                ]
                if result_message:
                    result_lines.append(result_message)
                if fm_message:
                    result_lines.append(fm_message)

                screen.fill(WHITE)
                for i, line in enumerate(result_lines):
                    screen.blit(font.render(line, True, BLACK), (220, 150 + i * 30))

                pygame.display.flip()
                pygame.time.wait(3000)
                return (money_change, hp_change, 0)

            # 게이지 자동 증가
            if now - last_auto_time >= 1.0 and now - last_skip_time >= 1.0:
                last_auto_time = now
                gauge += 0.5
                if gauge >= max_gauge:
                    game_over = True
                    result_message = "술을 너무 많이 마셔서 토했습니다! 🤮"
                    hp_change -= 20
                    money_change -= 5000

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    cooldown_elapsed = now - last_skill_time
                    if event.key == pygame.K_1 and cooldown_elapsed >= skill_cooldowns[1]:
                        last_skill_time = now
                        last_skip_time = now
                        if random.random() < 0.25:
                            hp_change -= 3
                            debuff_message = "걸렸습니다! 체력 -3"
                            debuff_time = now
                        else:
                            skill_effect_message = "스킬 효과 발동! (1초간 게이지 정지)"
                            skill_effect_time = now

                    elif event.key == pygame.K_2 and cooldown_elapsed >= skill_cooldowns[2]:
                        last_skill_time = now
                        gauge = max(0, gauge - 2)
                        if random.random() < 0.2:
                            hp_change -= 10
                            fm_message = "당신은~ 누구십니까~FM~FM~"
                            debuff_message = fm_message
                            debuff_time = now
                        else:
                            skill_effect_message = "스킬 효과 발동! (게이지 -3)"
                            skill_effect_time = now

                    elif event.key == pygame.K_3 and cooldown_elapsed >= skill_cooldowns[3]:
                        last_skill_time = now
                        if random.random() < 0.5:
                            hp_change -= 3
                            gauge += 1
                            debuff_message = "걸렸습니다! 체력 -3, 게이지 +1"
                            debuff_time = now
                        else:
                            gauge = max(0, gauge - 1)
                            skill_effect_message = "스킬 효과 발동! (게이지 -1)"
                            skill_effect_time = now

                    elif event.key == pygame.K_4 and not skill4_used:
                        skill4_used = True
                        gauge = 0
                        skill_effect_message = "스킬 효과 발동! (게이지 초기화)"
                        skill_effect_time = now

            # 게이지 바
            pygame.draw.rect(screen, DARKGRAY, (100, 100, 600, 40))
            pygame.draw.rect(screen, RED, (100, 100, int(600 * (gauge / max_gauge)), 40))
            screen.blit(font.render(f"주량 게이지: {gauge:.1f} / {max_gauge}", True, BLACK), (300, 150))

            # 남은 시간
            remain = max(0, int(duration - elapsed))
            screen.blit(font.render(f"남은 시간: {remain}초", True, BLACK), (330, 30))

            # 스킬 버튼 UI
            skills = ["1. 꺾어마시기", "2. 화장실", "3. 몰래버리기", "4. 숙취해소제"]
            cooldowns = [skill_cooldowns[1], skill_cooldowns[2], skill_cooldowns[3], 0]
            for i, label in enumerate(skills):
                x, y = 80 + i * 170, 450
                if i == 3:
                    color = GREEN if not skill4_used else DARKGRAY
                else:
                    color = GREEN if now - last_skill_time >= cooldowns[i] else DARKGRAY
                pygame.draw.rect(screen, color, (x, y, 160, 50), border_radius=8)
                txt = font.render(label, True, WHITE)
                screen.blit(txt, (x + 10, y + 10))

            # 효과 메시지
            if debuff_message and now - debuff_time <= 3:
                screen.blit(font.render(debuff_message, True, (200, 0, 0)), (230, 220))
            if skill_effect_message and now - skill_effect_time <= 3:
                screen.blit(font.render(skill_effect_message, True, (0, 180, 0)), (230, 260))

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    pygame.display.set_caption("미니게임 테스트")
    #minigame().professor_card_matching()
    minigame().eta_review_minigame