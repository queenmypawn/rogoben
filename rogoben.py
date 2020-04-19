#rogoben.py DAG file

# Step 1: Import all necessary packages.

# For scheduling
import datetime as dt

# For function jsonToCsv
import pandas as pd

# For function csvToSql
import csv
import pymysql

# Backwards compatibility of pymysql to mysqldb
pymysql.install_as_MySQLdb()

# Importing MySQLdb now
import MySQLdb

# For Apache Airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Step 2: Define functions for operators.

# A JSON string reader to .csv writer function.
def jsonToCsv(url, outputcsv):

    # Reads the JSON string into a pandas DataFrame object.
    data = pd.read_json(url)

    # Convert the object to a .csv file.
    # It is unnecessary to separate the JSON reading and the .csv writing.
    data.to_csv(outputcsv)

    return 'Read JSON and written to .csv'

def csvToSql():

    # Attempt connection to a database
    try:
        dbconnect = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='databasepwd',
                db='mydb'
                )
    except:
        print('Can\'t connect.')

    # Define a cursor iterator object to function and to traverse the database.
    cursor = dbconnect.cursor()

    # Create the table (if not yet created) using SQL statements.
    try:
        cursor.execute('CREATE TABLE rogobenDB3(number VARCHAR(255), docusignid VARCHAR(255), \
                publicurl VARCHAR(255), filingtype VARCHAR(255), \
                cityagencyname VARCHAR(255), cityagencycontactname VARCHAR(255), \
                cityagencycontacttelephone VARCHAR(255), \
                cityagencycontactemail VARCHAR(255), bidrfpnumber VARCHAR(255), \
                natureofcontract MEDIUMTEXT, datesigned VARCHAR(255), \
                comments VARCHAR(255), filenumber VARCHAR(255), \
                originalfilingdate VARCHAR(255), amendmentdescription VARCHAR(255), \
                additionalnamesrequired VARCHAR(255), signername VARCHAR(255), \
                signertitle VARCHAR(255))'
                )
    except:
        print('Table already exists; continuing to insert data.')
        
        '''
        # Check if table exists - DEBUG PURPOSES ONLY
        cursor.execute("SHOW TABLES")
        for db in cursor:
        print (db)
        '''
    # Open and read from the .csv file
    with open('./rogoben.csv') as csv_file:

        # Assign the .csv data that will be iterated by the cursor.
        csv_data = csv.reader(csv_file)

        # Insert data using SQL statements and Python
        for row in csv_data:
            cursor.execute(
            'INSERT INTO rogobenDB3(number, docusignid, publicurl, filingtype, \
                    cityagencyname, cityagencycontactname, \
                    cityagencycontacttelephone, cityagencycontactemail, \
                    bidrfpnumber, natureofcontract, datesigned, comments, \
                    filenumber, originalfilingdate, amendmentdescription, \
                    additionalnamesrequired, signername, signertitle) ' \
                    'VALUES("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", \
                    "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")',
                    row
                    )

    # Commit the changes
    dbconnect.commit()

    '''
    # Print all rows - FOR DEBUGGING ONLY
    cursor.execute("SELECT * FROM rogobenDB3")
    rows = cursor.fetchall()

    print(cursor.rowcount)
    for row in rows:
        print(row)
    '''

    # Close the connection
    cursor.close()

    # Confirm completion
    return 'Read .csv and written to the MySQL database'

# Step 3: Define the DAG, i.e. the workflow

# DAG's arguments
default_args = {
        'owner': 'rogoben',
        'start_date':dt.datetime(2020, 4, 16, 11, 00, 00),
        'concurrency': 1,
        'retries': 0
        }

# DAG's operators, or bones of the workflow
with DAG('parsing_govt_data',
        catchup=False, # To skip any intervals we didn't run
        default_args=default_args,
        schedule_interval='* 1 * * * *', # 's m h d mo y'; set to run every minute.
        ) as dag:

    opr_json_to_csv = PythonOperator(
            task_id='json_to_csv',
            python_callable=jsonToCsv,
            op_kwargs={
                'url':'https://data.sfgov.org/resource/pv99-gzft.json',
                'outputcsv':'./rogoben.csv'
                }
            )

    opr_csv_to_sql = PythonOperator(
            task_id='csv_to_sql',
            python_callable=csvToSql
            )

# The actual workflow
opr_json_to_csv >> opr_csv_to_sql
