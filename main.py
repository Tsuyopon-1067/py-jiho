from Clock import Clock
from queue import Queue
from SoundPlayer import Sound, SoundPlayer
from concurrent.futures import ThreadPoolExecutor


def main() -> None:
    soundqueue: Queue[Sound] = Queue()

    clock: Clock = Clock(soundqueue)
    soundplayer: SoundPlayer = SoundPlayer(soundqueue)

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(clock.run)
        executor.submit(soundplayer.run)


if __name__ == "__main__":
    main()
