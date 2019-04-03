from flask import Flask, Markup, request, redirect, render_template, url_for, g

import sqlite3
import statistics

app = Flask(__name__)


@app.route('/')
def home():
  return render_template("home.html")

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')