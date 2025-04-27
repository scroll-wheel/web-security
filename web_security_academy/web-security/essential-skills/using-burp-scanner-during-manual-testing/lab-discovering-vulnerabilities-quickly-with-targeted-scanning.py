from importlib import import_module

module = import_module("web_security_academy.web-security.xxe.lab-xinclude-attack")
solve_lab = getattr(module, "solve_lab")
