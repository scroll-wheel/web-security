#!/usr/bin/env python3

from importlib import import_module

if __name__ == "__main__":
    module = import_module("web-security.main")
    main = getattr(module, "main")
    main()
