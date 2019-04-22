import sqlite3, csv, pandas

conn = sqlite3.connect('store.db')
c = conn.cursor()

df = pandas.read_csv('./db.csv')
df.to_sql('store', conn, if_exists='append', index=False)

c.execute("select * from store")

print(c.fetchall())
