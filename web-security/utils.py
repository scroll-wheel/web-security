def print_success(string, end="\n"):
    print(f"\r\033[1;92m[+]\033[00m {string}", end=end)


def print_warning(string, end="\n"):
    print(f"\r\033[1;93m[!]\033[00m {string}", end=end)


def print_info(string, end="\n"):
    print(f"\r\033[1;94m[*]\033[00m {string}", end=end)


def print_info_secondary(string, end="\n"):
    print(f"\r\033[0;36m[?]\033[00m {string}", end=end)


def print_fail(string):
    print(f"\r\033[1;91m[-]\033[00m {string}")
    exit(1)
