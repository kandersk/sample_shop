import sqlite3
from flask import current_app as app
DATABASE = 'store.db'

def get_db():
  #conn = sqlite3.connect('students_v1.db')
  conn = sqlite3.connect(DATABASE)
  c = conn.cursor()
  return c

def get_item_info(itemNumber):
  dict = {}
  db = get_db()
  price = db.execute("select price from store where item = '{}'".format(itemNumber))
  title = db.execute("select title from store where item = '{}'".format(itemNumber))
  url = db.execute("select url from store where item = '{}'".format(itemNumber))
  qty = db.execute("select qty from store where item = '{}'".format(itemNumber))
  desc = db.execute("select desc from store where item = '{}'".format(itemNumber))
  shp = db.execute("select shp from store where item = '{}'".format(itemNumber))
  dict['itemNumber'] = itemNumber
  dict['price'] = price
  dict['title'] = title
  dict['url'] = url
  dict['quantity'] = qty
  dict['description'] = desc
  dict['Shipping price'] = shp
  return dict


bob = get_item_info(6)
print(bob)