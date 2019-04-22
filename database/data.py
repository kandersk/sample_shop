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
    db.execute("select item from store where title like '%{}'".format(word))
    matches = db.fetchall()
    matches_dict = []
    for i in matches:
        matches_dict.append(get_item_info(i[0]))
    return matches_dict


# db = get_db(DATABASE)
# item = (1,2,3,4,5,7,8,9)
# price = (2.99,5.66,798.4,4.5,666,734.6,69.69,12.34)
# title = ("thing1","thing2","thing3","thing4","thing5","kindle 2","kindle 3","kindle is bad")
# url = ("thing1","thing2","thing3","thing4","thing5","thing6","thing7","thing8")
# qty = (1,2,3,4,5,6,7,8)
# desc = ("thing1","thing2","thing3","thing4","thing5","thing6","thing7","thing8")
# shp = (1.99,2.99,3.99,4.99,5.99,6.99,7.99,8.99)


# for i in range(len(item)):
#     query = "insert into store (item,price,title,url,qty,desc,shp) VALUES({i1},{i2},'{i3}','{i4}',{i5},'{i6}',{i7});".format(i1 = item[i], i2 = price[i], i3 = title[i], i4 = url[i],i5 = qty[i], i6 = url[i],i7 = shp[i])
#     db.execute(query)

# for i in range(9):
#     print(get_item_info(i))

search_string = "kindle 1"
foo = get_matchs(search_string)
print(foo)
