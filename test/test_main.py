import os
import pytest
import csv, sqlite3  # For CSV->sqlite loading


# Loads the CSV file listed in the db.
# WARNING! This is specific to the UAnalytics csv file as only 2 fields are integers.
def load_CSV(csv_filename, db_filename):
    with open(csv_filename, 'r') as fin:
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        column_names = dr.fieldnames
        column_string = "','".join(column_names)
        # create columns in the DB based on the column names on the first row of CSV
        con = sqlite3.connect(db_filename)
        cur = con.cursor()
        integer_fields = ['item', 'qty']  # treat all others as strings
        string_fields = filter(lambda s: s not in integer_fields, column_names)
        string_fields_as_string = "','".join(string_fields)
        int_fields = filter(lambda s: s in integer_fields, column_names)
        cur.execute("CREATE TABLE items ('{}');".format(string_fields_as_string))  # TODO: use ? rather than format
        for field in int_fields:
            cur.execute("ALTER TABLE items ADD '{}' INTEGER;".format(field))  # TODO: use ? rather than format

        for row in dr:
            try:
                values = map(lambda column_name: row[column_name], column_names)
                values_string = "','".join(values)
            except:
                print("Error on line data {}".format(str(row)))
                assert False
            s = "INSERT INTO items ('{}') VALUES ('{}');".format(column_string,values_string)  # TODO: use ? rather than format
            cur.execute(s)
        con.commit()
        con.close()


from main import app


@pytest.fixture
def full_db_data_client():
    client = app.test_client()
    yield client


# A custom fixture which uses test_data_1.csv as the db
@pytest.fixture
def test1_db_data_client():
    testing_db = 'testing.db'
    if os.path.exists(testing_db):
        os.unlink(testing_db)  # Delete testing db just in case
    load_CSV('test/test_data_1.csv', testing_db)
    app.config['DB_PATH'] = testing_db
    client = app.test_client()

    yield client

    os.unlink(testing_db)  # Delete testing database


def test_description(test1_db_data_client):
    rv = test1_db_data_client.post('/3230576')
    assert b'92' in rv.data
    assert b'25.47' in rv.data
    assert b'11.99' in rv.data
    rv = test1_db_data_client.post('/3312435')
    assert b'8' in rv.data
    assert b'99.99' in rv.data
    assert b'17.99' in rv.data