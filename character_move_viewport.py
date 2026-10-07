"""pico2d ??? ?? ??."""

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1024


def main():
    import pico2d as p

    p.open_canvas(WINDOW_WIDTH, WINDOW_HEIGHT)
    try:
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
            p.update_canvas()
            p.delay(0.01)
    finally:
        p.close_canvas()


if __name__ == '__main__':
    main()
