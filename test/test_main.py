import os
import pytest
import csv, sqlite3 # For CSV->sqlite loading

# Loads the CSV file listed in the db. 
# WARNING! This is specific to the UAnalytics csv file as only 2 fields are integers.
def load_CSV(csv_filename, db_filename):
  with open(csv_filename,'r') as fin: 
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    column_names = dr.fieldnames
    column_string = "','".join(column_names)
    # create columns in the DB based on the column names on the first row of CSV 
    con = sqlite3.connect(db_filename)
    cur = con.cursor() 
    integer_fields = ['Grad year', 'Salary']  # treat all others as strings
    string_fields = filter(lambda s: s not in integer_fields, column_names)
    string_fields_as_string = "','".join(string_fields)
    int_fields = filter(lambda s: s in integer_fields, column_names)
    cur.execute("CREATE TABLE students ('{}');".format(string_fields_as_string)) # TODO: use ? rather than format
    for field in int_fields:
      cur.execute("ALTER TABLE students ADD '{}' INTEGER;".format(field)) # TODO: use ? rather than format
    for row in dr:
      values = map(lambda column_name: row[column_name], column_names)
      values_string = "','".join(values)
      s = "INSERT INTO students ('{}') VALUES ('{}');".format(column_string, values_string) # TODO: use ? rather than format
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
  #os.unlink(testing_db)  # Delete testing db just in case
  load_CSV('test/test_data_1.csv',testing_db)
  app.config['DB_FILENAME'] = testing_db
  client = app.test_client()

  yield client

  os.unlink(testing_db)  # Delete testing database

'''
Testing plan
1. Test that the button on Major report page returns sensable data when clicked
2. Do the same thing for compare report and minor report 
3. Test that on the sex report that I am returned sensable data 
'''
'''
def test_major_POST(full_db_data_client):
    rv = full_db_data_client.post('/major', data={'major': 'VCD'}) 
    assert b'48,956' in rv.data
'''
# Verify the majors listed to choose are all those in the test DB
def test_majors_listed(test1_db_data_client):
  rv = test1_db_data_client.get('/major') 
  # Only a handful of majors are in there:
  majors = ['AACT','ACPA','ACTS','AGNP','ANAT','ANTH','CHEM','BIOL','EMOT','NNP','PSYC','VCD']
  for m in majors:
    assert str.encode(m) in rv.data  # endocode converts the string to a bytestring to match data


def test_major_mean(test1_db_data_client):
    rv = test1_db_data_client.post('/major', data={'major': 'AGNP'}) 
    #print(rv.data)
    assert b'42,000' in rv.data   # it is finding 420000 instead of 42,000
    rv = test1_db_data_client.post('/major', data={'major': 'VCD'}) 
    assert b'50,200' in rv.data






