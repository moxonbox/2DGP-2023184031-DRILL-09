"""pico2d ??? ?? ??."""

from pathlib import Path

RESOURCE_DIR = Path(__file__).resolve().parent

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
DRAW_WIDTH = 100
DRAW_HEIGHT = 100
FRAME_COUNT = 8
ROWS = {('IDLE', 'RIGHT'): 3, ('IDLE', 'LEFT'): 2,
        ('RUN', 'RIGHT'): 1, ('RUN', 'LEFT'): 0}


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
        running = True
        while running:
            for event in p.get_events():
                if event.type == p.SDL_QUIT or (
                    event.type == p.SDL_KEYDOWN and event.key == p.SDLK_ESCAPE
                ):
                    running = False
            if not running:
                break
            p.clear_canvas()
            background.draw(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT)
            character.clip_draw(
                frame * FRAME_WIDTH, ROWS[state, facing] * FRAME_HEIGHT,
                FRAME_WIDTH, FRAME_HEIGHT, x, y, DRAW_WIDTH, DRAW_HEIGHT,
            )
            p.update_canvas()
            p.delay(0.01)
    finally:
        p.close_canvas()


if __name__ == '__main__':
    main()
