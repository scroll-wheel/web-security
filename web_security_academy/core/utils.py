from web_security_academy.core.logger import logger
from bs4 import BeautifulSoup
from pathlib import Path

import requests
import jinja2
import inspect
import os


def get_input(string):
    return input(f"\r\033[1;95m▌\033[00m {string}")


def auth_lab_usernames():
    resp = requests.get(
        "https://portswigger.net/web-security/authentication/auth-lab-usernames"
    )
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("code")
    result = query.text.split("\n")
    logger.info("Loaded Authentication lab usernames into memory")
    return result


def auth_lab_passwords():
    resp = requests.get(
        "https://portswigger.net/web-security/authentication/auth-lab-passwords"
    )
    soup = BeautifulSoup(resp.text, "lxml")
    query = soup.select_one("code")
    result = query.text.split("\n")
    logger.info("Loaded Authentication lab passwords into memory")
    return result


def generate_csrf_html(req, referrer=True):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
    template = env.get_template("csrf.html")
    html = template.render(req=req, referrer=referrer)
    return BeautifulSoup(html, "lxml").prettify()


def read_file(filename):
    file_path = os.path.abspath((inspect.stack()[1])[1])
    dir_path = os.path.dirname(file_path)
    with open(Path(dir_path) / filename, "rb") as f:
        return f.read()


def render_template_file(filename, **kwargs):
    file_path = os.path.abspath((inspect.stack()[1])[1])
    dir_path = os.path.dirname(file_path)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(dir_path))
    template = env.get_template(filename)
    return template.render(**kwargs)
