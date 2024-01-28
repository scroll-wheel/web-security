from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests import Session

from .exploit_server import ExploitServer


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
