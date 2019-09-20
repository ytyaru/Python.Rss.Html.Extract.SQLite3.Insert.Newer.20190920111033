#!/usr/bin/env python3
# coding: utf8
import sys
import os
import extractcontent3

class HtmlContentExtractor:
    def __init__(self, option=None):
        self.__html = None
        self.__text = None
        self.__extractor = extractcontent3.ExtractContent()
        if option is not None: self.__extractor.set_option(option) # option = {"threshold":50}
    @property
    def Html(self): return self.__html
    @property
    def Text(self): return self.__text
    def extract(self, html):
        self.__extractor.analyse(html)
#        text, title = extractor.as_text()
        self.__html, title = self.__extractor.as_html()
#        title = extractor.extract_title(html)
        self.__text = self.__format_to_text(html)
        return self.__text
    def __format_to_text(self, html):
        import re
        import unicodedata
        st = re.sub(r"<p>([^　])", r"　\1", html) # 段落の先頭は全角スペース
        st = re.sub(r"</p>", "\n\n", st) # 段落の末尾は2つ改行する
        st = re.sub(r"</br>", "\n", st)
        st = re.sub(r"<br>", "\n", st)
        st = re.sub(r"<.+?>", "", st)
        # Convert from wide character to ascii
        if st and type(st) != str: st = unicodedata.normalize("NFKC", st)
        st = re.sub(r"[\u2500-\u253f\u2540-\u257f]", "", st)  # 罫線(keisen)
#        st = re.sub(r"&(.*?);", lambda x: self.CHARREF.get(x.group(1), x.group()), st)
        st = re.sub(r"[ \t]+", " ", st)
        return st.rstrip("\n\t ")
    def __show_meta(self):
        print('extractcontent3 メタ情報')
        print(extractcontent3.__version__)
        print(extractcontent3.__file__)
        print(dir(extractcontent3))

