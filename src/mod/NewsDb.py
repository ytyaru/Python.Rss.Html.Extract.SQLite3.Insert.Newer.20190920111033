import sqlite3
import os
import operator

class NewsDb:
    def __init__(self, root):
        path = os.path.join(root, 'news.db')
        self.conn = sqlite3.connect(path)
        self.create_table()
        self.news = []
    def __del__(self): self.conn.close()
    def create_table(self):    
        cur = self.conn.cursor()
        cur.executescript(self.__create_table_sql())
    def __create_table_sql(self):
        return '''
create table if not exists news(
  id         integer primary key,
  published  text,
  url        text,
  title      text,
  body       text  -- URL先から本文だけを抽出したプレーンテキスト
);
create index if not exists idx_news on 
  news(published desc, id desc, url, title);
create table if not exists sources(
  id       integer primary key,
  domain   text, -- URLのドメイン名
  name     text, -- 情報源名
  created  text  -- 登録日時（同一ドメイン名が複数あるとき新しいほうを表示する）
);
create index if not exists idx_sources on 
  sources(domain, created desc, id desc, name);
'''
    def __get_latest_sql(self): return '''
with 
  latest(max_published) as (
    select max(published) max_published from news
  )
select 
  published as latest_published, 
  max(id) as latest_id 
from news,latest
where news.published=latest.max_published;
'''
    def __is_get_latest(self):
        cur = self.conn.cursor()
#        row = cur.execute(self.__get_latest_sql()).fetchone()
#        if row is None: return None
#        published, url = rows[0]
#        return published, url
        return cur.execute(self.__get_latest_sql()).fetchone()

    def __get_newer_news(self):
        self.news = sorted(self.news, key=operator.itemgetter(1)) # 第2キー: URL昇順
        self.news = sorted(self.news, key=operator.itemgetter(0), reverse=True) # 第1キー: 公開日時降順
        latest_published, latest_url = self.__is_get_latest() # DB最新
        if latest_published is None: return self.news # DBが0件なら全件挿入する

        # JSON最古がDB最新より新しければ全件挿入する
        if self.news[len(self.news)-1][0] > latest_published: return self.news
        # JSON最新がDB最新と同じか古ければ挿入しない
        if (self.news[0][0] < latest_published or
           (self.news[0][0] == latest_published and 
            self.news[0][1] == latest_url)): return None
        # JSON内にDB最新が存在する
        try: 
            # 先頭からDB最新+1までを挿入する
            idx = self.news.index((latest_published, latest_url))
            return self.news[0:idx]
        # JSON内にDB最新が存在しない
        except ValueError:
            # JSON先頭がDB最新より新しいなら全件挿入する
            if self.news[0][0] > latest_published: return self.news
            # JSON先頭がDB最新かそれより古いなら挿入しない
            else: return None

    def __insert_sql(self): 
        return 'insert into news(published,url,title,body) values(?,?,?,?)'
    def append_news(self, published, url, title, body):
        self.news.append((published, url, title, body))
    def insert(self):
        if 0 == len(self.news): return
        try:
            ins_news = self.__get_newer_news()
            if ins_news is None: return
            cur = self.conn.cursor()
            cur.executemany(self.__insert_sql(), ins_news)
            self.conn.commit()
            self.news.clear()
        except: 
            import traceback
            traceback.print_exc()
            self.conn.rollback()
#        finally: self.news.clear()

