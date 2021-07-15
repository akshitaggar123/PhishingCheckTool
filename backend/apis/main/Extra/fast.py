import asyncio
import aiohttp
from aiohttp import ClientSession, ClientConnectorError
from generator import Domain_generator

async def fetch_html(url: str, session: ClientSession, **kwargs) -> tuple:
    try:
        resp = await session.request(method="GET", url=url, **kwargs)
    except:
        return (url, 404)
    return (url, resp.status)

async def make_requests(urls: set, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                fetch_html(url=url, session=session, **kwargs)
            )
        results = await asyncio.gather(*tasks)

    for result in results:
        print(f'{result[1]} - {str(result[0])}')

url="https://www.google.com/"
g=Domain_generator(url)
possible_urls=sorted(g.generate_urls())
asyncio.run(make_requests(urls=possible_urls))