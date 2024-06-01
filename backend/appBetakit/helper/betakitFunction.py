import requests
import re
import datetime
import json
import asyncio
from pprint import pprint
from typing import Any
from bs4 import (BeautifulSoup as bs, )
from appBetakit.helper.aiFunction import AccessGPT, instr_core
from appBetakit.helper.wordReferencer import generate_related_words # must start from base file directory
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

"""
Tools:
Request wrapper
search wrapper
Souper (<- request wrapper, <- search wrapper)
"""

class HTMLSearch:
    """
    """
    def _single_item_check(self, single_bool: bool, input: list):
        if single_bool:
            if len(input) == 1:
                return input[0]
            else:
                return ValueError
        return input
    
    def childSearch_byParentClassTag(self, element, parent_tag, parent_classname, child_tag):
        return element.find(parent_tag, {'class': parent_classname}).findChild(child_tag)


class HTMLElementSearch(HTMLSearch):
    """Returns an element after a search.
    """
    
    def divSearch_byClass(self, element, classname, single: bool=False):
        result = element.find_all("div", {"class": classname})

        return self._single_item_check(single_bool=single, input=result)

    def searchChildren_byTag(self, element, tag: str, single: bool=False):
        result = element.findChildren(tag)

        return self._single_item_check(single_bool=single, input=result)
    
    def childSearch_byParentClassTag(self, element, parent_tag, parent_classname, child_tag):
        return super(HTMLElementSearch, self).childSearch_byParentClassTag(
            element=element,
            parent_tag=parent_tag,
            parent_classname=parent_classname,
            child_tag=child_tag
        )
        
    def search_byClass(
        self,
        element,
        tag: str,
        classname: str,
        class_string: str
    ):
        raise NotImplementedError
    
    def search_inChildren(
        self,
        element,
        tag: str,
    ):
        raise NotImplementedError


class HTMLTextSearch(HTMLSearch):
    """Returns an element after a text.
    """

    def spanSearch_byClass(self, element, classname, single: bool=False):
        result = element.find_all("span", {"class": classname})

        return self._single_item_check(single_bool=single, input=result).text
    
    def childSearch_byParentClassTag(self, element, parent_tag, parent_classname, child_tag):
        return super(HTMLTextSearch, self).childSearch_byParentClassTag(
            element=element,
            parent_tag=parent_tag,
            parent_classname=parent_classname,
            child_tag=child_tag
        ).text


class SiteRequester:
    """
    """
    
    header: str
    body_content: str
    text_searcher: HTMLTextSearch
    element_searcher: HTMLElementSearch

    def __init__(self, header) -> None:
        self.header = header
        self.text_searcher = HTMLTextSearch()
        self.element_searcher = HTMLElementSearch()

    def set_url(self, url):
        ...


class BetakitScraper:
    """
    date formatting <- Look for some class
    title formatting combo text <- Look for some class
    Href support <- Look for some class

    target string <- regex search

    """
    ...


class BetakitFundingScraper(BetakitScraper):
    """Build ontop of BetakitScraper to scrape this: https://betakit.com/tag/funding/page/#/
    
    1. Send a request to get a main page: could be funding etc. <- request wrapper (get, header, )
    2. Get all the list of articles on the page: element retriever (<- souper, element count check)
    3. Format the articles to a list of tuples <- (<- search wrapper, datetime conversion, combo text <- search, HREF)'
    -- Use AI to find relevant articles
    4. Per article that is relevant, find elements that are relevant for GPT
    -- Use AI to generate summary
    
    SelectArticles
    """

    url: str
    header: str
    parser: str
    element_searcher: HTMLElementSearch
    text_searcher: HTMLTextSearch
    raw_articles: list
    articles: dict
    ai: AccessGPT

    def __init__(self, header, target_string) -> None:
        print('[Not Started] Initializing ...')
        self.url = 'https://betakit.com/tag/funding/page/{0}/'
        self.header = header
        self.parser = 'html.parser'
        self.element_searcher = HTMLElementSearch()
        self.text_searcher = HTMLTextSearch()
        self.ai = AccessGPT()
        self.target_string = target_string
        # self.target_string = 'Raised or someone invested more than 50 million into the company'
        self.target_word_reference = generate_related_words(self.target_string)
        self.raw_articles = []
        self.ai.set_system_instruction(instruction=instr_core)
        print('[In Progress] System set up ...')
        print('[In Progress] Gathering articles ...')
        self._find_articles()
        print('[In Progress] Formatting articles ...')
        self._format_articles()
        
        print('[In Progress] Finding important articles ...')
        self._ai_filter_articles()
        

        # Execute criterias to find the best potential article to analyze
        # Can use AI or use other search tools
        # Assume we found what we want, say item 1
        # self.filtered_articles = {
        #     0: self.articles[0],
        #     1: self.articles[1]
        # }
        print('[In Progress] Collecting based on criteria ...')
        self._iterate_articles() # uses a regex search
        self._create_summaries()
        print('[Done] Complete!')
        
        # pprint(self.filtered_articles)
        
    def _get_url_content(self, url):
        try:
            res = requests.get(url=url, headers=self.header)
            if res.status_code == 200:
                return res.content
            else:
                return ValueError
        except:
            return ValueError
         
    def _soup_content(self, url):
        content = self._get_url_content(url=url)
        return bs(content, self.parser)

    def _find_articles(self, max_page=3):

        for i in range(max_page):

            num = i+1
            print("++++++++++++++++++++++++++++++++++")
            print(num)

            soup = self._soup_content(url=self.url.format(num))
        
            article_block = self.element_searcher.divSearch_byClass(
                element=soup,
                classname='grids list-layout entries',
                single=True
            )
            
            self.raw_articles += self.element_searcher.searchChildren_byTag(
                element=article_block,
                tag='article'
            )
            print(len(self.raw_articles))

    def _format_one_article(self, article_chunk):
        
        try:
            # assume date format: May 23, 2023
            text_date = self.text_searcher.spanSearch_byClass(
                element=article_chunk,
                classname='entry-date',
                single=True
            )
            formatted_date = datetime.datetime.strptime(text_date, '%B %d, %Y')

            # Combo text
            title = self.text_searcher.childSearch_byParentClassTag(
                element=article_chunk,
                parent_tag='h2',
                parent_classname='entry-title',
                child_tag='a'
            )
            desc = self.text_searcher.childSearch_byParentClassTag(
                element=article_chunk,
                parent_tag='div',
                parent_classname='entry-summary',
                child_tag='p'
            )
            combo_text = title + '; ' + desc

            #href
            article_href = self.element_searcher.childSearch_byParentClassTag(
                element=article_chunk,
                parent_tag='h2',
                parent_classname='entry-title',
                child_tag='a'
            ).get('href')

            return {
                'date': formatted_date.isoformat(), 
                'title_description': combo_text, 
                'article_url': article_href
            }
        except Exception as e:
            print(f"Error in _format_one_article: {e}")
            raise  # Re-raise the exception to be caught in the calling method

    def _format_articles(self):
        self.articles = {}
        for idx, article in enumerate(self.raw_articles):
            self.articles[idx] = self._format_one_article(article)
    
    def _ai_comboText_search(self, combo_text):
        inp = self.ai.summary_analysis_inp(
            combo_text=combo_text,
            word=self.target_string
        ) 
        return self.ai.complete(inp=inp)
    
    def regex_aiValidCheck(self, text: str, value: str):
        search = re.search(value, text)
        if search is not None:
            return 1
        else:
            return 0
    
    def _ai_filter_articles(self):
        self.filtered_articles = {}

        for idx, article_dict in self.articles.items():
            ai_result = self._ai_comboText_search(article_dict['title_description'])
            look_out = self.regex_aiValidCheck(text=ai_result.content, value='1')
            if look_out == 1:
                self.filtered_articles[idx] = article_dict
        # for some reason this doesn't work, not sure why
        """
        
        async def _ai_comboText_search(self, combo_text):
            inp = self.ai.summary_analysis_inp(
                combo_text=combo_text,
                word=self.target_string
            ) 
            return await self.ai.complete(inp=inp)
        
        async def _ai_filter_articles(self):
            self.filtered_articles = {}
            for idx, article_dict in self.articles.items():
                task = self._ai_comboText_search(
                    combo_text=article_dict['title_description']
                )
                checker = await asyncio.gather(task)
                if int(checker.content) == 1: 
                    self.filtered_articles[idx] = article_dict
        
        """
    
    def get_filtered_articles(self):
        return self.filtered_articles
    
    def count_collected_articles(self):
        return len(self.articles)
    
    def count_filtered_articles(self):
        return len(self.filtered_articles)

    def _regex_search(self, soup:bs, target_string: str) -> list:
        return soup(text=re.compile(target_string, re.I))

    def _betakit_strip(self, elements: set) -> list:
        # filtered_elements = [
        #     f'{element.parent.name}; {str(element).strip()}' for element in elements
        #     if element.parent.name not in ['script', 'title', 'style']
        # ] #this is betakit specific
        filtered_elements = [
            str(element).strip() for element in elements
            if element.parent.name not in ['script', 'title', 'style']
        ] #this is betakit specific
        return filtered_elements

    def _check_content(self, soup: bs, target_string_list: list):
        """This is an exact search
        """
        regex_elements = []

        for target_string in target_string_list:
            temp = self._regex_search(soup=soup, target_string=target_string)
            regex_elements += temp

        return self._betakit_strip(elements=set(regex_elements))
    
    def _iterate_articles(self):
        for idx, dict_content in self.filtered_articles.items():
            soup_article = self._soup_content(url=dict_content['article_url'])
            elements = self._check_content(soup=soup_article, target_string_list=self.target_word_reference)
            self.filtered_articles[idx]['article_elements'] = elements

    def _create_summaries(self):
        for idx, dict_content in self.filtered_articles.items():
            inp = self.ai.content_analysis_inp(
                combo_text=dict_content['title_description'],
                word=self.target_string,
                content='; '.join(dict_content['article_elements'])
            )
            # print(inp)
            self.filtered_articles[idx]['summary'] = self.ai.complete(inp=inp).content



    
    def __str__(self) -> str:
        return f'Article stored count: {len(self.raw_articles)}'


if __name__ == '__main__':
    url="https://betakit.com/tag/funding/"
    main = BetakitFundingScraper(header=headers)
    # print(main)
