#!/usr/bin/env python3
# coding: utf8
import feedparser
import datetime
import sys
from mod import get_html
from mod import NewsDb
from mod import NewsImagesDb
from mod import HtmlContentExtractor

if len(sys.argv) < 2:
    raise Error('第1引数にRSSのURLを指定してください。')
    exit()
if len(sys.argv) < 3:
    raise Error('第2引数にSQLite3DBルートパスを指定してください。')
    exit()
rss = sys.argv[1]
db_dir_path = sys.argv[2]

entries = feedparser.parse(rss).entries
news_db = NewsDb.NewsDb(db_dir_path)
extractor = HtmlContentExtractor.HtmlContentExtractor()
for entry in entries:
    published = (datetime.datetime
        .strptime(entry.published, 
                  '%a, %d %b %Y %H:%M:%S %z')
        .strftime('%Y-%m-%dT%H:%M:%SZ%z'))
    url = entry.link
    title = entry.title
    body = extractor.extract(get_html.get_html(url))
    news_db.append_news(published, url, title, body);
    break; # HTML取得を1件だけでやめる
news_db.insert();

