# Readme


## legacy

1. go to raw and adjust `fetch.sh`
    - detect url
    - detect upper bound for chapters
2. adjust `src/main.py` ho much chapters to convert
3. go to gutenberg an download titlepage
4. in sigil
    - add title page
    - add all chapters (processed)
    - generate TOC
    - create epub


## pure python

1. detect baseurl and determine chapters
    - update [src/config.yaml]() accordingly
2. run [src/main.py]()
3. go to gutenberg an download titlepage
4. in sigil
    - add title page
    - add all chapters (processed)
    - generate TOC
    - add style (prosa.css)
    - create epub
