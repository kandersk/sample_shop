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

@app.route('/<id>')
def description(id):
  dic = get_item_info(id)
  url = dic['url']
  name = dic['title']
  desc = dic['desc']
  qty = dic['qty']
  price = dic['price']
  shipping = dic['shp']

  return render_template("description.html", url = url, name = name, desc = desc,qty = qty, price = price, shipping = shipping)


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
