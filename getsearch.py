import sqlite3
from data import get_db
from data import get_item_info
DATABASE = 'store.db'
def get_matchs(word):
    db = get_db(DATABASE)
    db.execute("select item from store having {} in title".format(word))
    matches = db.fetchall()
    matches_dict = ()
    for i in matches:
        matches_dict.append(get_item_info(i))
    return matches_dict

# db = get_db()
#
# db.execute("insert into store (item,price,title,url,qty,desc,shp) values(1,2.8,{thing},{url},4,{dsc},9.99)".format(thing="title",url="urlurl",dsc="thing,thing,thing"))
# db.execute("insert into store (item,price,title,url,qty,desc,shp) values(2,280.99,{thing},{url},6,{dsc},9.99)".format(thing="kindle 2",url="urlurl",dsc="shitty kindle 2.0"))
# db.execute("insert into store (item,price,title,url,qty,desc,shp) values(3,380.99,{thing},{url},5,{dsc},9.99)".format(thing="kindle 3",url="urlurl",dsc="shitty kindle 3.0"))

search_string = "kindle"
foo = get_matchs(search_string)
print(foo)
