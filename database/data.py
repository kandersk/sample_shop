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
  db.execute("select item,price,title,imageurl,qty,descrip,shp from store where item = {}".format(itemNumber))
  things = db.fetchall()
  key = ('itemNum','price','title','url','qty','desc','shp')
  dct = dict(zip(key,things[0]))

  return dct

def get_matchs(word):
    matches_dict = []
    db = get_db(DATABASE)
    db.execute("select item from store where instr(title,'{}') > 1".format(word))
    matches = db.fetchall()
    print(len(matches))
    for i in matches:
        matches_dict.append(get_item_info(i[0]))
    return matches_dict


# foo = get_item_info(6)
search_string = "Hex"
foo = get_matchs(search_string)
print(foo)
