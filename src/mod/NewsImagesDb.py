import sqlite3
import os

class NewsImagesDb:
    def __init__(self, root):
        path = os.path.join(root, 'news_images.db')
        self.conn = sqlite3.connect()
        self.create_table()
        self.stmts = []
    def __del__(self): self.conn.close()
    def create_table(self):    
        cur = self.conn.cursor()
        cur.execute(self.__create_table_sql())
    def __create_table_sql(self):
        return '''
create table if not exists images(
  news_id integer, -- どの記事に対応した画像か
  url     text,    -- 拡張子も含めているはず。これ重要
  image   blob     -- バイナリ
);'''
    def append_insert_stmt(self, news_id, url, image):
        self.stmts.append("insert into images(news_id, url, image) values("
            + "'" + news_id + "',"
            + "'" + url       + "',"
            + "'" + image      + "'"
            + ");");
    def insert(self):
        if 0 == len(self.stmts): return
        self.stmts.insert(0, "begin;")
        self.stmts.append("end;")
        cur = self.conn.cursor()
        cur.execute("\n".join(stmts))
        self.stmts.clear()

