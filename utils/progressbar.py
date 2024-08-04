import sys
import time


def progressbar(current, total, start):
    finish = "▓" * current
    need_do = "-" * (total - current)
    progress = (current / total) * 100
    dur = time.perf_counter() - start

    if current < total:
        print(
            "\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finish, need_do, dur), end=""
        )
    else:
        print(
            "\r{:^3.0f}%[{}] {:.2f}s".format(progress, finish, dur)
        )  # 在进度达到100%时允许print自动添加换行符

    sys.stdout.flush()
    time.sleep(1)
