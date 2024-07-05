from importlib import import_module

# Reuse exploit from "lab-basic-csrf-protected"
module = import_module(
    "web_security_academy.web-security.clickjacking.lab-basic-csrf-protected"
)
solve_lab = getattr(module, "solve_lab")
