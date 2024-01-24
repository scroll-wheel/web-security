from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests import Session

from .exploit_server import ExploitServer
from .utils import *


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
        print_info(f'Grabbing CSRF value from "{url}"...')

        resp = Session.get(self, url)
        soup = BeautifulSoup(resp.text, "html.parser")
        query = soup.select('input[name="csrf"]')

        if len(query) < n:
            print_fail("Unable to grab CSRF value.")
        else:
            csrf = query[n - 1].get("value")
            print_success(f"CSRF value: {csrf}\n")
        return csrf

    def login(self, username, password, with_csrf=True):
        if not with_csrf:
            data = {"username": username, "password": password}
        else:
            csrf = self.get_csrf_token("/login")
            data = {"csrf": csrf, "username": username, "password": password}

        print_info(
            f'Logging in with username "{username}" and password "{password}"...'
        )
        resp = self.post_path("/login", data=data)
        soup = BeautifulSoup(resp.text, "html.parser")
        invalid_creds = soup.find(text="Invalid username or password.")

        if invalid_creds:
            print_fail("Invalid credentials.")
        else:
            print_success("Successfully logged in.\n")

        return resp

    def submit_solution(self, answer):
        print_info(f'Submitting "{answer}" as solution...')
        url = urljoin(self.url, "/submitSolution")
        data = {"answer": answer}
        resp = Session.post(self, url, data=data)

        if resp.json()["correct"]:
            print_success("Correct answer!\n")
        else:
            print_fail("Incorrect answer.")

    def exploit_server(self):
        if not hasattr(self, "ExploitServer"):
            self.ExploitServer = ExploitServer(self)
        return self.ExploitServer
