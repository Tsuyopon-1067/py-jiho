from Clock import Clock
from queue import Queue
from SoundPlayer import Sound, SoundPlayer
from concurrent.futures import ThreadPoolExecutor
import light_sensor


def main() -> None:
    soundqueue: Queue[Sound] = Queue()  # スレッド間通信用 再生する音声情報をいれる

    clock: Clock = Clock(soundqueue)  # 時計を動かす
    soundplayer: SoundPlayer = SoundPlayer(soundqueue)  # soundqueueを監視して音声を鳴らす

    with ThreadPoolExecutor(max_workers=2) as executor:  # 以下の2つを別スレッドで動かす
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
