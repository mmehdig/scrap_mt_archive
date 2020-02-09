import re
import scrapy
from scrapy.crawler import CrawlerProcess

"""
TODO:
- unification of paper entities.
- parsing the paper citation text.
"""

authors = []
spliters = ['see,', 'see ,', ',']
papers = dict()

class AuthorSpider(scrapy.Spider):
    name = 'authorspider'
    start_urls = ['http://www.mt-archive.info/srch/authors.htm']

    def _rejoin_text(self, parts):
        return ' '.join(
            part.strip().replace('\t', ' ').replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('  ', ' ').strip()
            for part in parts
        ).strip()

    def parse(self, response):
        if response.url == self.start_urls[0]:
            for next_page in response.css('a'):
                next_url = next_page.css('::attr(href)').get()
                if next_url is not None and re.compile(r'.*srch/author.*').match(next_url):
                    yield response.follow(next_page, self.parse)

        prev_lastnames = tuple([])
        prev_firstnames = tuple([])
        prev_papers = []
        for any_item in response.css('div > p'):
            author_items = any_item.css('p>b')
            if len(author_items)==0:
                # paper parser:
                paper_text = any_item.xpath(".//text()").extract()
                paper_title = any_item.xpath(".//a/text()").extract()
                paper_url = any_item.xpath(".//a/@href").extract()
                paper_title = self._rejoin_text(paper_title)
                paper_text = self._rejoin_text(paper_text)

                if len(paper_url) > 0:
                    paper_url = paper_url[0]
                else:
                    paper_url = ''

                if (paper_title, paper_url) in papers:
                    papers[(paper_title, paper_url)]['text'].append(paper_text)
                    papers[(paper_title, paper_url)]['authors'].append((prev_firstnames, prev_lastnames))
                else:
                    papers[(paper_title, paper_url)] = {
                        'authors': [(prev_firstnames, prev_lastnames)],
                        'text': [paper_text],
                    }

                prev_papers.append((paper_title, paper_url, paper_text))
                continue

            authors.append((prev_firstnames, prev_lastnames, prev_papers))
            #yield {
            #    'lastnames': prev_lastnames,
            #    'firstnames': prev_firstnames,
            #    '#papers': len(prev_papers),
            #    'papers': prev_papers,
            #}
            # new author episod
            author_item = author_items[0]
            prev_papers = []

            # author parser:
            lastnames = author_item.css('*::text').getall()
            lastnames = [''.join(lastnames).strip()]
            for spliter in spliters:
                lastnames = [
                    lastname
                    for _lastnames in lastnames
                    for _lastname in _lastnames.split(spliter)
                    for lastname in [_lastname.strip()]
                    if len(lastname)>0
                ]
            if len(lastnames) == 0:
                continue
            lastname = lastnames[0]

            firstnames = author_item.css('*~*::text').getall()
            firstnames = [''.join(firstnames).strip()]
            for spliter in spliters:
                firstnames = [
                    firstname
                    for _firstnames in firstnames
                    for _firstname in _firstnames.split(spliter)
                    for firstname in [_firstname.strip()]
                    if len(firstname)>0
                ]
            if len(firstnames) == 0:
                continue
            firstname = firstnames[0]

            with open("authors.csv", "a") as authors_csv:
                authors_csv.write(f'"{firstname}", "{lastname}"\n')
                authors_csv.close()

            firstnames = tuple(firstnames)
            lastnames = tuple(lastnames)

            prev_lastnames = lastnames
            prev_firstnames = firstnames

process = CrawlerProcess()
process.crawl(AuthorSpider)
process.start()
#print(papers)
for fnames, lnames, apapers in authors:
    if 'Johansson' in fnames and 'Richard' in lnames:
        for paper_text, paper_url, _ in  apapers:
            print(papers[(paper_text, paper_url)])
