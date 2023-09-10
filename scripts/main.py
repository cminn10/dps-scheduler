import time
from booking_script import exec_booking, send_email
from config import RUN_DURATION, RUN_INTERVAL, SHOULD_SEND_EMAIL


def start_job(duration, interval):
    start_time = time.time()
    loop_completed = True
    while time.time() - start_time < duration:
        res = exec_booking()
        if res:
            loop_completed = False
            break
        time.sleep(interval)
    if loop_completed and SHOULD_SEND_EMAIL:
        send_email('Job finished without available slots.')


if __name__ == '__main__':
    start_job(RUN_DURATION, RUN_INTERVAL)
