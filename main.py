import re
import aiohttp
import asyncio
import jsonlines

from bs4 import BeautifulSoup as bs

base_url = "https://google.com"

headers = dict()
params = dict()
cookies = dict()


async def number_of_pages(session):
    async with session.get(f'{base_url}?pg=1', headers=headers, params=params, cookies=cookies) as response:
        response = await response.text()
        soup = bs(response, 'html.parser')
        __number_of_pages__ = int(soup.find('span', class_="total").get_text())
        return __number_of_pages__


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()

        data = await response.text()
        return data


async def fetch_all_page_deals(session, urls):
    tasks = [asyncio.create_task(fetch(session, url))
             for url in urls]
    for task in asyncio.as_completed(tasks):
        yield await task


def page_deals(source):
    source = "https://google.com"
    deal_urls = list()
    return deal_urls


def parse_deal(session, url, queue):
    # parsing is hidden
    my_dict = dict()
    await queue.put(my_dict)


async def consumer(queue):
    while True:
        lines = await queue.get()
        if lines is None:
            break
        # Write to file. I'd recommend using a threadpool to do this,
        # via run_in_executor, as filesystem IO will block otherwise.
        # There's not currently a good OS-level API for async filesystem IO.
        loop = asyncio.get_event_loop()
        # Where path is a path-like or string, and lines is a
        # list of each line to write to the file. You can probably parse the
        # lines using each result from the queue.
        path = "deals.jsonl"
        await loop.run_in_executor(None, write_to_file, path, lines)

        # Note: loop.run_in_executor uses the format of:
        # run_in_executor(executor, func, *args). Specifying None
        # as *executor* uses the default ThreadPoolExecutor.


# Would like to convert this to jsonlines
def write_to_file(path, lines):
    with jsonlines.open(path, 'a') as writer:
        for line in lines:
            writer.write(line)


async def main():
    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()
        # nos = await number_of_pages(session)
        nos = 1

        async for page_deal in fetch_all_page_deals(session, nos):
            # Parse IN-Store & Online upc, sku, title, price, location
            await asyncio.gather(parse_deal(session, page_deal, queue), consumer(queue))


if __name__ == '__main__':
    asyncio.run(main())
