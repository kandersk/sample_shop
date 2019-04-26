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


  return render_template("search.html",t = t, results = results)

@app.route('/<id>', methods = ['GET','POST'])
def description(id):
  dic = get_item_info(id)
  url = dic['url']
  name = dic['title']
  desc = dic['desc']
  qty = dic['qty']
  price = dic['price']
  shipping = dic['shp']

  return render_template("description.html", url = url, name = name, desc = desc,qty = qty, price = price, shipping = shipping, id = id)

@app.route('/<id>/cart', methods = ['GET','POST'])
def cart(id):
  dic = get_item_info(id)
  url = dic['url']
  name = dic['title']
  price = dic['price']
  shipping = dic['shp']
  if request.method == 'POST':
    qtyC = request.form['qty']
    priceQty = round(float(qtyC)*price, 2)
    total = round(float(qtyC)*price + shipping, 2)
    return render_template("cart.html",qtyC = qtyC, url = url, name = name,priceQty = priceQty, shipping = shipping, total = total)
  return render_template("cart.html", url = url, name = name)


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
