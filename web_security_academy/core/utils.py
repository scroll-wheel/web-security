import inspect
import os
from pathlib import Path

import jinja2
from bs4 import BeautifulSoup


def bs4(markup):
    return BeautifulSoup(markup, "lxml")


def get_input(string):
    return input(f"\r\033[1;95m▌\033[00m {string}")


def generate_csrf_html(req, referrer=True):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))
    template = env.get_template("csrf.html")
    html = template.render(req=req, referrer=referrer)
    return bs4(html).prettify()


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
