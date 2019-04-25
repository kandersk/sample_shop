#!/usr/bin/env python3

from flask import Flask, Markup, request, redirect, render_template, url_for, g

import sqlite3
import statistics

app = Flask(__name__)
DATABASE = 'database/store.db'

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/search', methods = ['GET','POST'])
def search():
    t = {'Search': ""}
    if request.method =='POST':
        t['Search'] = request.form['Search']
    results = get_matchs(t['Search'])


  # {'itemNum': 3220024, 'price': 14.97,
  # 'title': "'Hex head cap screw M12x1.25-40 (box/50)'",
  # 'url': "'https://www.mcmaster.com/mvB/Contents/gfx/ImageCache/913/91309A628p1-b01-digital@100p_636824767630548193.png'",
  # 'qty': 4, 'desc': "'Hex head cap screw M12x1.25-40 (box/50)'",
  # 'shp': 5.99}

  # search bar that accepts product by name
  # submit accepts the form input
  # sends to database as query
  # retrieves database results
  # parses results
  # formats on template
    return render_template("search.html",t = t, results = results)

@app.route('/description', methods = ['GET','POST'])
def description():
  dic = get_item_info(3245337)
  url = dic['url']
  name = dic['title']
  desc = dic['desc']
  qty = dic['qty']
  price = dic['price']
  shipping = dic['shp']

  if request.method == 'POST':
    qtyC = request.form['qty']
    return render_template("cart.html",qtyC = qtyC)
  else:
    return render_template("description.html", url = url, name = name, desc = desc,qty = qty, price = price, shipping = shipping)

@app.route('/cart', methods = ['GET','POST'])
def cart():
  dic = get_item_info(3245337)
  url = dic['url']
  name = dic['title']
  price = dic['price']
  shipping = dic['shp']
  if request.method == 'POST':
    qtyC = request.form['qty']
    subtotal = round(float(qtyC)*price + shipping, 2)
    if qtyC == 1:
      pl = "item"
    else:
      pl = "items"
    return render_template("cart.html",qtyC = qtyC, url = url, name = name, subtotal = subtotal, pl = pl)
  return render_template("cart.html", qtyC = [], url = url, name = name, subtotal = [], pl = [])


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
  db.execute("select item from store where title like '%{}%'".format(word))
  matches = db.fetchall()
  print(len(matches))
  for i in matches:
    matches_dict.append(get_item_info(i[0]))
  return matches_dict


if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')
