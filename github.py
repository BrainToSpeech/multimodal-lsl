# paradigm_fixed_carousel.py
# 고정 3단계(Cue→Action→Rest) 테스트 루퍼 (LSL markers 포함)

import os, time, pygame
from pygame.locals import *
from pylsl import StreamInfo, StreamOutlet, local_clock

# ===== 설정 =====
FULLSCREEN   = False
WIN_SIZE     = (1920, 1080)
FPS          = 60

N_TRIALS     = 1        # 반복 횟수 (원하면 변경)
CUE_SEC      = 2.0
ACTION_SEC   = 2.0
REST_SEC     = 2.0

FONT_NAME    = r"C:\Windows\Fonts\malgun.ttf"
FONT_SIZE    = 72
BG           = (0, 0, 0)
FG           = (255, 255, 255)

# ===== LSL 이벤트 코드 =====
event_id_map = {
    "READY":  0,
    "CUE":    11,
    "ACTION": 12,
    "REST":   13,
    "END":    99,
}

# ===== 공용 렌더/대기 =====
def draw_text(screen, text, font, color=FG):
    screen.fill(BG)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(surf, rect)
    pygame.display.flip()

def wait_fixed(seconds, clock, draw_frame):
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < seconds:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); raise SystemExit
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit(); raise SystemExit
        draw_frame()
        clock.tick(FPS)

# ===== LSL =====
def make_marker_outlet():
    info = StreamInfo(
        name="BCI_Markers",
        type="Markers",
        channel_count=1,
        nominal_srate=0,
        channel_format="string",
        source_id="paradigm_fixed_carousel_v1",
    )
    info.desc().append_child_value("app", "paradigm_fixed_carousel")
    return StreamOutlet(info)

def send_code(outlet, code: int):
    outlet.push_sample([str(code)], local_clock())

# ===== 메인 =====
def main():
    # LSL
    outlet = make_marker_outlet()
    send_code(outlet, event_id_map["READY"])
    print("Fixed 3-step paradigm ready. Press ENTER to start, ESC to quit.")
    try:
        input()
    except EOFError:
        pass

    # 화면
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    flags = pygame.FULLSCREEN if FULLSCREEN else 0
    screen = pygame.display.set_mode(WIN_SIZE, flags)
    pygame.display.set_caption("Fixed Cue–Action–Rest (CSV-free)")
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    # 안내
    def draw_wait():
        draw_text(screen, "Press SPACE to start", font)
    # SPACE 누르면 시작
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); raise SystemExit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit(); raise SystemExit
                if event.key == K_SPACE:
                    break
        else:
            draw_wait()
            clock.tick(FPS)
            continue
        break

    # ===== 트라이얼 루프 =====
    for t in range(1, N_TRIALS + 1):
        # CUE (2s)
        send_code(outlet, event_id_map["CUE"])
        wait_fixed(CUE_SEC, clock, lambda: draw_text(screen, "cue", font))

        # ACTION (2s)
        send_code(outlet, event_id_map["ACTION"])
        wait_fixed(ACTION_SEC, clock, lambda: draw_text(screen, "action", font))

        # REST (2s)
        send_code(outlet, event_id_map["REST"])
        wait_fixed(REST_SEC, clock, lambda: draw_text(screen, "rest", font))

    # 종료
    draw_text(screen, "Session End", font)
    send_code(outlet, event_id_map["END"])
    wait_fixed(1.0, clock, lambda: None)
    pygame.quit()

if __name__ == "__main__":
    main()
