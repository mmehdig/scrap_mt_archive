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

For example these two papers are the same but with two different URLs:
```
>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', '05/CoNLL-2009-Hajic.pdf')]['text'][0]
'(2009) Jan Hajič, Massimiliano Ciaramita, Richard Johansson, Daisuke Kawahara, Maria Antònia Marti, Lluís Màrquez, Adam Meyers, Joakim Nivre, Sebastian Padó, Jan Štěpánek, Pavel Straňák, Mihai Surdeanu, Nainwen Xue, & Yi Zhang: The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages . CoNLL-2009. Proceedings of the Thirteenth Conference on Computational Natural Language Learning: Shared Task , June 4, 2009, Boulder , Colorado ; pp.1-18. [PDF, 220KB]'

>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', 'CoNLL-2009-Hajic.pdf')]['text'][0]
'(2009) Jan Hajič, Massimiliano Ciaramita, Richard Johansson, Daisuke Kawahara, Maria Antònia Marti, Lluís Màrquez, Adam Meyers, Joakim Nivre, Sebastian Padó, Jan Štěpánek, Pavel Straňák, Mihai Surdeanu, Nainwen Xue, & Yi Zhang: The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages . CoNLL-2009. Proceedings of the Thirteenth Conference on Computational Natural Language Learning: Shared Task , June 4, 2009, Boulder , Colorado ; pp.1-18. [PDF, 220KB]'

>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', 'http://www.mt-archive.info/CoNLL-2009-Hajic.pdf')]['text'][0]
'(2009) Jan Hajič, Massimiliano Ciaramita, Richard Johansson, Daisuke Kawahara, Maria Antònia Marti, Lluís Màrquez, Adam Meyers, Joakim Nivre, Sebastian Padó, Jan Štěpánek, Pavel Straňák, Mihai Surdeanu, Nainwen Xue, & Yi Zhang: The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages . CoNLL-2009. Proceedings of the Thirteenth Conference on Computational Natural Language Learning: Shared Task , June 4, 2009, Boulder , Colorado ; pp.1-18. [PDF, 220KB]'
```

Consequently, the authors are not linked to the same paper:
```
>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', '05/CoNLL-2009-Hajic.pdf')]['authors']
[(('Joakim',), ('Nivre',)), (('Adam',), ('Meyers',))]

>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', 'CoNLL-2009-Hajic.pdf')]['authors']
[(('Massimiliano',), ('Ciaramita',)), (('Yun [Susan]', 'Susan'), ('Xu',)), (('Yi',), ('Zhang',)), (('Jan',), ('Štěpánek',)), (('Pavel',), ('Straňák',)), (('Mihai',), ('Surdeanu',)), (('Jan',), ('Hajič',))]

>>> papers[('The CoNLL-2009 Shared task: syntactic and semantic dependencies in multiple languages', 'http://www.mt-archive.info/CoNLL-2009-Hajic.pdf')]['authors']
[(('Sebastian',), ('Padó',)), (('Sebastian',), ('Padó',)), (('Richard',), ('Johansson',)), (('Lluís',), ('Màrquez',)), (('Maria Antònia',), ('Martí',)), (('Daisuke',), ('Kawahara',))]
```
