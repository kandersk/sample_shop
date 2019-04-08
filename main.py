#!/usr/bin/env python3

from flask import Flask, Markup, request, redirect, render_template, url_for, g

import sqlite3
import statistics

app = Flask(__name__)


@app.route('/')
def home():
  return render_template("home.html")

@app.route('/search')
def search():

  # search bar that accepts product by name
  # submit accepts the form input
  # sends to database as query
  # retrieves database results
  # parses results
  # formats on template

  return render_template("search.html")

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')