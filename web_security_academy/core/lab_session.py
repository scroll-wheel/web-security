import socket
import ssl
from time import sleep
from urllib.parse import urljoin, urlparse

import certifi
import h2
import httpx
import requests
import urllib3

from .exploit_server import ExploitServer
from .logger import logger
from .utils import bs4


class LabSession:
    def __init__(self, url, use_httpx=True, use_proxy=False):
        self.use_httpx = use_httpx
        if use_httpx:
            if use_proxy:
                logger.debug('Using "http://127.0.0.1:8080" as a proxy')
                self.client = httpx.Client(
                    proxy="http://127.0.0.1:8080",
                    verify=False,
                )
                self.async_client = httpx.AsyncClient(
                    proxy="http://127.0.0.1:8080",
                    verify=False,
                )
            else:
                self.client = httpx.Client()
                self.async_client = httpx.AsyncClient()
        else:
            if use_proxy:
                logger.debug('Using "http://127.0.0.1:8080" as a proxy')
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                self.client = requests.Session()
                self.client.proxies.update(
                    {
                        "http": "http://127.0.0.1:8080",
                        "https": "http://127.0.0.1:8080",
                    }
                )
                self.client.verify = False
            else:
                self.client = requests.Session()

        self.url = urljoin(url, "/")
        self.hostname = urlparse(self.url).hostname
        self.cookies = self.client.cookies

    def get_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.get(url, **kwargs)

    async def a_get_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.get(url, **kwargs)

    def head_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.head(url, **kwargs)

    async def a_head_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.head(url, **kwargs)

    def options_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.options(url, **kwargs)

    async def a_options_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.options(url, **kwargs)

    def post_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.post(url, **kwargs)

    async def a_post_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.post(url, **kwargs)

    def put_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.put(url, **kwargs)

    async def a_put_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.put(url, **kwargs)

    def patch_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.path(url, **kwargs)

    async def a_patch_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.patch(url, **kwargs)

    def delete_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.client.delete(url, **kwargs)

    async def a_delete_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return self.async_client.delete(url, **kwargs)

    def get_csrf_token(self, path, n=1):
        logger.trace(f'Grabbing CSRF value from "{path}"...')
        resp = self.get_path(path)
        soup = bs4(resp.text)
        query = soup.select('input[name="csrf"]')

        if len(query) < n:
            logger.failure(f'Unable to grab CSRF value from "{path}"')
            exit(1)
        else:
            csrf = query[n - 1].get("value")
            logger.debug(f'CSRF value from "{path}": {csrf}')
        return csrf

    async def a_get_csrf_token(self, path, n=1):
        logger.trace(f'Grabbing CSRF value from "{path}"...')
        resp = await self.a_get_path(path)
        soup = bs4(resp.text)
        query = soup.select('input[name="csrf"]')

        if len(query) < n:
            logger.failure(f'Unable to grab CSRF value from "{path}"')
            exit(1)
        else:
            csrf = query[n - 1].get("value")
            logger.debug(f'CSRF value from "{path}": {csrf}')
        return csrf

    def login(self, username, password, with_csrf=True, with_json=False):
        if not with_csrf:
            data = {"username": username, "password": password}
        else:
            csrf = self.get_csrf_token("/login")
            data = {"csrf": csrf, "username": username, "password": password}

        logger.trace(
            f'Logging in with username "{username}" and password "{password}"...'
        )

        if with_json:
            resp = self.post_path("/login", json=data, follow_redirects=True)
        else:
            resp = self.post_path("/login", data=data, follow_redirects=True)

        soup = bs4(resp.text)
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

    async def a_login(self, username, password, with_csrf=True, with_json=False):
        if not with_csrf:
            data = {"username": username, "password": password}
        else:
            csrf = await self.a_get_csrf_token("/login")
            data = {"csrf": csrf, "username": username, "password": password}

        logger.trace(
            f'Logging in with username "{username}" and password "{password}"...'
        )

        if with_json:
            resp = await self.a_post_path("/login", json=data, follow_redirects=True)
        else:
            resp = await self.a_post_path("/login", data=data, follow_redirects=True)

        soup = bs4(resp.text)
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
        resp = self.post_path("/submitSolution", data={"answer": answer})

        if resp.json()["correct"]:
            logger.success(f'Submitted answer "{answer}" is correct!')
        else:
            logger.failure(f'Submitted answer "{answer}" is incorrect')

    async def a_submit_solution(self, answer):
        logger.trace(f'Submitting "{answer}" as solution...')
        resp = await self.a_post_path("/submitSolution", data={"answer": answer})

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

    def send_raw(self, req):
        address = ("localhost", 8080) if self.proxies else (self.hostname, 443)
        with socket.create_connection(address) as sock:
            if self.proxies:
                sock.sendall(f"CONNECT {self.hostname}:443 HTTP/1.1\r\n\r\n".encode())
                sock.recv(65536 * 1024)

            ctx = ssl._create_unverified_context()
            with ctx.wrap_socket(sock, server_hostname=self.hostname) as sock:
                sock.sendall(req)

                resp = b""
                while True:
                    data = sock.recv(65536 * 1024)
                    resp += data
                    if not data:
                        break
                return resp

    def auth_lab_usernames(self):
        resp = self.client.get(
            "https://portswigger.net/web-security/authentication/auth-lab-usernames",
            proxy=None,
        )
        soup = bs4(resp.text)
        query = soup.select_one("code")
        result = query.text.split("\n")
        logger.info("Loaded Authentication lab usernames into memory")
        return result

    def auth_lab_passwords(self):
        resp = self.client.get(
            "https://portswigger.net/web-security/authentication/auth-lab-passwords",
            proxy=None,
        )
        soup = bs4(resp.text)
        query = soup.select_one("code")
        result = query.text.split("\n")
        logger.info("Loaded Authentication lab passwords into memory")
        return result
