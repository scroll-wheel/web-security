from web_security_academy.core.lab_session import LabSession
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from httpx import AsyncClient
from bs4 import BeautifulSoup


class AsyncLabSession(AsyncClient):
    # Todo: Add workers
    def __init__(self, LabSession):
        if not LabSession.proxies:
            proxies = None
            verify = True
        else:
            proxies = LabSession.proxies["http"]
            verify = False

        AsyncClient.__init__(self, http2=True, proxies=proxies, verify=verify)
        self.url = LabSession.url

    async def get_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return await AsyncClient.get(self, url, **kwargs)

    async def post_path(self, path, **kwargs):
        url = urljoin(self.url, path)
        return await AsyncClient.post(self, url, **kwargs)

    async def get_csrf_token(self, path, n=1):
        url = urljoin(self.url, path)
        logger.trace(f'Grabbing CSRF value from "{path}"...')

        resp = await AsyncClient.get(self, url)
        soup = BeautifulSoup(resp.text, "html.parser")
        query = soup.select('input[name="csrf"]')

        if len(query) < n:
            logger.failure(f'Unable to grab CSRF value from "{path}"')
            exit(1)
        else:
            csrf = query[n - 1].get("value")
            logger.debug(f'CSRF value from "{path}": {csrf}')
        return csrf

    async def login(self, username, password, with_csrf=True):
        if not with_csrf:
            data = {"username": username, "password": password}
        else:
            csrf = await self.get_csrf_token("/login")
            data = {"csrf": csrf, "username": username, "password": password}

        logger.trace(
            f'Logging in with username "{username}" and password "{password}"...'
        )
        resp = await self.post_path("/login", data=data)
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

    async def submit_solution(self, answer):
        logger.trace(f'Submitting "{answer}" as solution...')
        url = urljoin(self.url, "/submitSolution")
        data = {"answer": answer}
        resp = await AsyncClient.post(self, url, data=data)

        if resp.json()["correct"]:
            logger.success(f'Submitted answer "{answer}" is correct!')
        else:
            logger.failure(f'Submitted answer "{answer}" is incorrect')
