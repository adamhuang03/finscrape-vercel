import sys
import os
import asyncio
from pprint import pprint
sys.path.append(os.path.join(os.path.dirname(__file__))) # go to parent dir
from betakitFunction import BetakitFundingScraper
from aiFunction import AccessGPT, headers

async def call_async():
    url="https://betakit.com/tag/funding/"
    betakit = BetakitFundingScraper(url=url, header=headers)
    await betakit._ai_filter_articles()
    return betakit

def call(inp):
    url="https://betakit.com/tag/funding/"
    betakit = BetakitFundingScraper(url=url, header=headers, target_string=inp)
    return betakit

if __name__ == '__main__':
    # x = asyncio.run(call())
    # Raised or someone invested more than 50 million into the company
    inp = input("Enter your criteria: ")
    x = call(inp=inp)
    # print(len(x.articles))
    # print(len(x.filtered_articles))
    # pprint(x.filtered_articles)
    print(f'Found: {len(x.articles)}\nFiltered: {len(x.filtered_articles)}\n\n')
    for idx, dct in x.filtered_articles.items():
        pprint(dct['summary'])

