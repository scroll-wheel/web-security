from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests import Session

from .exploit_server import ExploitServer

import certifi
import ssl
import socket
import h2
from time import sleep


class LabSession(Session):
    def __init__(self, url):
        Session.__init__(self)
        self.url = urljoin(url, "/")

    def get_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return Session.get(self, url, **kwargs)

    def post_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return Session.post(self, url, **kwargs)

    def get_csrf_token(self, path, n=1):
        url = urljoin(self.url, path)
        logger.trace(f'Grabbing CSRF value from "{path}"...')

        resp = Session.get(self, url)
        soup = BeautifulSoup(resp.text, "html.parser")
        query = soup.select('input[name="csrf"]')

        if len(query) < n:
            logger.failure(f'Unable to grab CSRF value from "{path}"')
            exit(1)
        else:
            csrf = query[n - 1].get("value")
            logger.debug(f'CSRF value from "{path}": {csrf}')
        return csrf

    def login(self, username, password, with_csrf=True):
        if not with_csrf:
            data = {"username": username, "password": password}
        else:
            csrf = self.get_csrf_token("/login")
            data = {"csrf": csrf, "username": username, "password": password}

        logger.trace(
            f'Logging in with username "{username}" and password "{password}"...'
        )
        resp = self.post_path("/login", data=data)
        soup = BeautifulSoup(resp.text, "html.parser")
        invalid_creds = soup.find(text="Invalid username or password.")

        if invalid_creds:
            logger.failure(
                f'Unable to log in with username "{username}" and password "{password}"'
            )
        else:
            logger.info(
                f'Logged in with username "{username}" and password "{password}"'
            )

        return resp

    def submit_solution(self, answer):
        logger.trace(f'Submitting "{answer}" as solution...')
        url = urljoin(self.url, "/submitSolution")
        data = {"answer": answer}
        resp = Session.post(self, url, data=data)

        if resp.json()["correct"]:
            logger.success(f'Submitted answer "{answer}" is correct!')
        else:
            logger.failure(f'Submitted answer "{answer}" is incorrect')

    def exploit_server(self):
        if not hasattr(self, "ExploitServer"):
            self.ExploitServer = ExploitServer(self)
        return self.ExploitServer

    # TODO: Make this work through a proxy
    def single_packet_send(self, *prepared_requests):
        # Set up SSL socket wrapper
        ctx = ssl.create_default_context(cafile=certifi.where())
        ctx.set_alpn_protocols(["h2"])

        # Set up socket
        hostname = urlparse(self.url).hostname
        sock = socket.create_connection((hostname, 443))
        sock = ctx.wrap_socket(sock, server_hostname=hostname)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 0)

        # Set up H2 connection
        conn = h2.connection.H2Connection()
        conn.initiate_connection()
        sock.sendall(conn.data_to_send())

        # Only accept HTTP responses with no encoding
        for req in prepared_requests:
            req.headers["Accept-Encoding"] = "identity"

        # Send partial requests
        stream_ids = []
        base_headers = [(":authority", hostname), (":scheme", "https")]
        for i, r in enumerate(prepared_requests):
            path = urlparse(r.url).path + "?" + urlparse(r.url).query
            headers = base_headers + [(":method", r.method), (":path", path)]
            headers += list(r.headers.items())

            stream_ids.append(conn.get_next_available_stream_id())
            conn.send_headers(stream_ids[i], headers)
            if (r.body is not None) and (len(r.body) > 1):
                conn.send_data(stream_ids[i], r.body[:-1].encode())
            sock.sendall(conn.data_to_send())

        # Wait and warm up connection
        sleep(0.1)
        headers = base_headers + [(":method", "GET"), (":path", "/")]
        conn.send_headers(conn.get_next_available_stream_id(), headers, end_stream=True)
        sock.sendall(conn.data_to_send())

        # Send single packet finishing all reqeusts
        for i, r in enumerate(prepared_requests):
            if (r.body is not None) and (len(r.body) > 1):
                conn.send_data(stream_ids[i], r.body[-1].encode(), end_stream=True)
            else:
                conn.end_stream(stream_ids[i])
        sock.sendall(conn.data_to_send())

        responses = [
            {"headers": None, "data": b""} for _ in range(len(prepared_requests) + 1)
        ]

        ended_streams = 0
        while ended_streams < len(prepared_requests) + 1:
            data = sock.recv(65536 * 1024)
            if not data:
                break

            events = conn.receive_data(data)
            for event in events:
                if isinstance(event, h2.events.ResponseReceived):
                    headers = [(k.decode(), v.decode()) for k, v in event.headers]
                    responses[event.stream_id // 2]["headers"] = dict(headers)
                if isinstance(event, h2.events.DataReceived):
                    conn.acknowledge_received_data(
                        event.flow_controlled_length, event.stream_id
                    )
                    responses[event.stream_id // 2]["data"] += event.data
                if isinstance(event, h2.events.StreamEnded):
                    decoded = responses[event.stream_id // 2]["data"].decode()
                    responses[event.stream_id // 2]["data"] = decoded
                    ended_streams += 1

        conn.close_connection()
        sock.sendall(conn.data_to_send())

        sock.close()
        return responses[:-1]

    # Todo: Add proxy functionality
    def send_raw(self, req):
        hostname = urlparse(self.url).hostname
        with socket.create_connection((hostname, 443)) as sock:
            ctx = ssl.create_default_context(cafile=certifi.where())
            with ctx.wrap_socket(sock, server_hostname=hostname) as sock:
                sock.sendall(req)

                resp = b""
                while True:
                    data = sock.recv(65536 * 1024)
                    resp += data
                    if not data:
                        break
                return resp
