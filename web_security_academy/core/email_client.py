from bs4 import BeautifulSoup
from .utils import *
from urllib.parse import urljoin
import re


class EmailClient:
    def __init__(self, session):
        self.session = session

        print_info("Determining email client URL...")

        resp = session.get_path("/")
        soup = BeautifulSoup(resp.text, "html.parser")
        exploit_link = soup.select_one("#exploit-link")

        if exploit_link is None:
            print_fail("Unable to find email client URL.")
        else:
            self.url = exploit_link.get("href")
            print_success(f"Email client URL: {self.url}\n")

        self.update_emails()

    def update_emails(self):
        resp = self.session.get(self.url)
        soup = BeautifulSoup(resp.text, "html.parser")
        h4 = soup.select_one("h4")
        self.address = re.match("Your email address is (.*)", h4.text).group(1)

        query = soup.select("table tr:not(:first-child)")
        query.reverse()

        self.emails = []
        for row in query:
            soup = BeautifulSoup(str(row), "html.parser")
            data = soup.select("td")
            email = {
                "Sent": data[0].text,
                "To": data[1].text,
                "From": data[2].text,
                "Subject": data[3].text,
                "Body": data[4].text,
            }
            self.emails.append(email)
