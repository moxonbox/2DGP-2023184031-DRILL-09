"""pico2d ??? ?? ??."""

from math import hypot
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
MOVE_SPEED = 300
MAX_DT = 0.05
LOOP_DELAY = 0.01
ROWS = {('IDLE', 'RIGHT'): 3, ('IDLE', 'LEFT'): 2,
        ('RUN', 'RIGHT'): 1, ('RUN', 'LEFT'): 0}


def move_position(x, y, dx, dy, dt):
    """?? ??? ????? ?? ???? ????."""
    length = hypot(dx, dy)
    if length:
        x += dx / length * MOVE_SPEED * dt
        y += dy / length * MOVE_SPEED * dt
    x = max(DRAW_WIDTH / 2, min(x, WINDOW_WIDTH - DRAW_WIDTH / 2))
    return x, y


def main():
    try:
        import pico2d as p
    except ModuleNotFoundError as error:
        if error.name == 'pico2d':
            raise SystemExit('pico2d? ?????: python -m pip install pico2d') from error
        raise

    for name in ('TUK_GROUND.png', 'animation_sheet.png'):
        path = RESOURCE_DIR / name
        if not path.is_file():
            raise FileNotFoundError(f'??? ??? ????: {path}')

    p.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
        background = p.load_image(str(RESOURCE_DIR / 'TUK_GROUND.png'))
        character = p.load_image(str(RESOURCE_DIR / 'animation_sheet.png'))
        x, y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        state, facing = 'IDLE', 'RIGHT'
        frame = 0
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
    main()
