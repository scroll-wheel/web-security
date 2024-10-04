from web_security_academy.core.logger import logger

from bs4 import BeautifulSoup
import re


class EmailClient:
    def __init__(self, session):
        self.session = session

        logger.debug("Determining email client URL...")

        resp = session.get_path("/")
        soup = BeautifulSoup(resp.text, "lxml")
        exploit_link = soup.select_one("#exploit-link")

        if exploit_link is None:
            logger.failure("Unable to find email client URL.")
            exit(1)
        else:
            self.url = exploit_link.get("href")
            logger.info(f"Email client URL: {self.url}")

        self.update_emails()

    def update_emails(self):
        resp = self.session.get(self.url)
        soup = BeautifulSoup(resp.text, "lxml")
        h4 = soup.select_one("h4")
        self.address = re.match("Your email address is (.*)", h4.text).group(1)

        query = soup.select("table tr:not(:first-child)")
        query.reverse()

        self.emails = []
        for row in query:
            soup = BeautifulSoup(str(row), "lxml")
            data = soup.select("td")
            email = {
                "Sent": data[0].text,
                "To": data[1].text,
                "From": data[2].text,
                "Subject": data[3].text,
                "Body": data[4],
            }
            self.emails.append(email)
