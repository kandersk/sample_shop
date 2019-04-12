import sqlite3
from flask import current_app as app
DATABASE = 'store.db'

def get_db(DATABASE):
  #conn = sqlite3.connect('students_v1.db')
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  return c

def get_item_info(itemNumber):
  db = get_db(DATABASE)
  db.execute("select item,price,title,url,qty,desc,shp from store where item = {}".format(itemNumber))
  things = db.fetchall()
  key = ('itemNum','price','title','url','qty','desc','shp')
  dct = dict(zip(key,things[0]))

  return dct

def get_matchs(word):
    db = get_db(DATABASE)
    db.execute("select item from store having {} in title".format(word))
    matches = db.fetchall()
    matches_dict = ()
    for i in matches:
        matches_dict.append(get_item_info(i))
    return matches_dict

search_string = "kindle"
foo = get_matchs(search_string)
print(foo)
