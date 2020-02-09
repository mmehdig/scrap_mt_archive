## Scrap MT Archive
This is a mini-project to strap MT Archive into xml format for ACL Anthology.

## Requirements
Python3 packages:

- scrapy


## Information about `author_scrap.py`

### How to run
For debug:

```
python3 -i author_scrap.py
```

Then you can inspect `papers` and `authors`.

### How it words

The Scrapy Spider crawls the pages from [here](http://www.mt-archive.info/srch/authors.htm).
Finds all **bold** author name, creates tuples for firstname alternatives and lastname alternatives per author.
Then, for each paper citation under each author name, it creates a paper entity with url and title and authors, and citation text.

### Known bugs
Each paper entity is specified with its title and url.
However, sometimes there are more than one url mentioned over the website.
Another process is needed to unify these papers based on other factors, such as year, authors and journal or conference name.
