from importlib import import_module

# Explanation: Since token validation depends on the token being present, I
# don't need to supply a CSRF token in my payload. Therefore, I can reuse my
# exploit from "lab-no-defenses".

module = import_module(f"web_security_academy.web-security.csrf.lab-no-defenses")
solve_lab = getattr(module, "solve_lab")(session)
