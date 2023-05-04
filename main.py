from Clock import Clock
from queue import Queue
from SoundPlayer import Sound, SoundPlayer
from concurrent.futures import ThreadPoolExecutor
import light_sensor


def main() -> None:
    soundqueue: Queue[Sound] = Queue()

    clock: Clock = Clock(soundqueue)
    soundplayer: SoundPlayer = SoundPlayer(soundqueue)

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(clock.run)
        executor.submit(soundplayer.run)


if __name__ == '__main__':
    try:
        light_sensor.setup_gpio()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        light_sensor.cleanup()
