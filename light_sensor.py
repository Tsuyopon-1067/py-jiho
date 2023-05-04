# https://pimylifeup.com/raspberry-pi-light-sensor/

import RPi.GPIO as GPIO

pin_to_circuit = 7


def setup_gpio() -> None:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_to_circuit, GPIO.IN)


def is_open() -> bool:
    return GPIO.input(pin_to_circuit) == GPIO.HIGH


def cleanup() -> None:
    return GPIO.cleanup()


if __name__ == '__main__':
    from time import sleep
    setup_gpio()
    try:
        while True:
            print(
                f'Lights are {"on" if GPIO.input(pin_to_circuit) else "off"}.')
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
