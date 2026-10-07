"""pico2d 캐릭터 이동 데모."""

from math import hypot, isclose
import sys
from pathlib import Path
from time import perf_counter

RESOURCE_DIR = Path(__file__).resolve().parent

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
DRAW_WIDTH = 100
DRAW_HEIGHT = 100
FRAME_COUNT = 8
IDLE_INTERVAL = 0.125
RUN_INTERVAL = 0.1
MOVE_SPEED = 300
MAX_DT = 0.05
LOOP_DELAY = 0.01
ROWS = {('IDLE', 'RIGHT'): 3, ('IDLE', 'LEFT'): 2,
        ('RUN', 'RIGHT'): 1, ('RUN', 'LEFT'): 0}


def move_position(x, y, dx, dy, dt):
    """입력 벡터를 정규화하여 시간 기반으로 이동한다."""
    length = hypot(dx, dy)
    if length:
        x += dx / length * MOVE_SPEED * dt
        y += dy / length * MOVE_SPEED * dt
    x = max(DRAW_WIDTH / 2, min(x, WINDOW_WIDTH - DRAW_WIDTH / 2))
    y = max(DRAW_HEIGHT / 2, min(y, WINDOW_HEIGHT - DRAW_HEIGHT / 2))
    return x, y


def self_test():
    """창과 pico2d 없이 이동·정규화·경계 규칙을 검증한다."""
    center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    assert move_position(*center, 0, 0, 0.05) == center
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)):
        x, y = move_position(*center, dx, dy, 0.05)
        assert isclose(hypot(x - center[0], y - center[1]), 15, abs_tol=1e-9)
    left, right = DRAW_WIDTH / 2, WINDOW_WIDTH - DRAW_WIDTH / 2
    bottom, top = DRAW_HEIGHT / 2, WINDOW_HEIGHT - DRAW_HEIGHT / 2
    for x, dx in ((left, -1), (right, 1)):
        for y, dy in ((bottom, -1), (top, 1)):
            assert move_position(x, y, dx, dy, 10) == (x, y)
            moved_x, moved_y = move_position(*center, dx, dy, 10)
            assert left <= moved_x <= right and bottom <= moved_y <= top
    x, y = center
    for _ in range(5):
        x, y = move_position(x, y, 1, 0, 0.01)
    assert isclose(x, move_position(*center, 1, 0, 0.05)[0], abs_tol=1e-9)
    print('이동·대각선 속도·뷰포트 경계 검증 통과')


def main():
    if not (0 < DRAW_WIDTH <= WINDOW_WIDTH and 0 < DRAW_HEIGHT <= WINDOW_HEIGHT):
        raise ValueError('뷰포트 크기는 캐릭터 출력 크기 이상이어야 합니다.')
    try:
        import pico2d as p
    except ModuleNotFoundError as error:
        if error.name == 'pico2d':
            raise SystemExit('pico2d가 필요합니다: python -m pip install pico2d') from error
        raise

    for name in ('TUK_GROUND.png', 'animation_sheet.png'):
        path = RESOURCE_DIR / name
        if not path.is_file():
            raise FileNotFoundError(f'리소스 파일이 없습니다: {path}')

    p.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        background = p.load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        character = p.load_image(str(RESOURCE_DIR / 'animation_sheet.png'))
        x, y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        state, facing = 'IDLE', 'RIGHT'
        frame = 0
        animation_elapsed = 0.0
        pressed_keys = set()
        arrow_keys = {p.SDLK_LEFT, p.SDLK_RIGHT, p.SDLK_UP, p.SDLK_DOWN}
        previous_time = perf_counter()
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT or (
                    event.type == p.SDL_KEYDOWN and event.key == p.SDLK_ESCAPE
                ):
                    running = False
                elif event.type == p.SDL_KEYDOWN and event.key in arrow_keys:
                    pressed_keys.add(event.key)
                elif event.type == p.SDL_KEYUP and event.key in arrow_keys:
                    pressed_keys.discard(event.key)
            if not running:
                break
            now = perf_counter()
            dt = min(now - previous_time, MAX_DT)
            previous_time = now
            dx = int(p.SDLK_RIGHT in pressed_keys) - int(p.SDLK_LEFT in pressed_keys)
            dy = int(p.SDLK_UP in pressed_keys) - int(p.SDLK_DOWN in pressed_keys)
            if dx < 0:
                facing = 'LEFT'
            elif dx > 0:
                facing = 'RIGHT'
            x, y = move_position(x, y, dx, dy, dt)
            next_state = 'RUN' if dx or dy else 'IDLE'
            if next_state != state:
                state = next_state
                frame = 0
                animation_elapsed = 0.0
            interval = RUN_INTERVAL if state == 'RUN' else IDLE_INTERVAL
            animation_elapsed += dt
            while animation_elapsed >= interval:
                animation_elapsed -= interval
                frame = (frame + 1) % FRAME_COUNT
            p.clear_canvas()
            background.draw(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
            character.clip_draw(
                frame * FRAME_WIDTH, ROWS[state, facing] * FRAME_HEIGHT,
                FRAME_WIDTH, FRAME_HEIGHT, x, y, DRAW_WIDTH, DRAW_HEIGHT,
            )
            p.update_canvas()
            p.delay(LOOP_DELAY)
    finally:
        p.close_canvas()


if __name__ == '__main__':
    if sys.argv[1:] == ['--self-test']:
        self_test()
    else:
        main()
