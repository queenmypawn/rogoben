# These are the libraries used for this project.
import gspread
import mysql.connector
from oauth2client.service_account import ServiceAccountCredentials

# This is the mysqlcredentials.py file containing your credentials.
import mysqlcredentials as mc

# The required variables for gspread:
scope = ['https://spreadsheets.google.com/feeds', \
	'https://www.googleapis.com/auth/drive']

# The credentials created for the service account in your Google project
# is stored in a .json file after you click 'Create Key'
# I renamed this file to sheetstodb.json.
creds = ServiceAccountCredentials.from_json_keyfile_name('sheetstodb.json', scope)
client = gspread.authorize(creds)

# Now that that's done, pull data from the Google sheet.
# 'sheetName' describes the Google sheet's name,
# 'worksheetIndex' describes the index of the worksheet at the bottom.
def GetSpreadsheetData(sheetName, worksheetIndex):
    sheet = client.open(sheetName).get_worksheet(worksheetIndex)
    return sheet.get_all_values()[1:]

# Finally, write this data to MySQL:
def WriteToMySQLTable(sql_data, tableName):
    try:
# Connection credentials for MySQL.
        connection = mysql.connector.connect(
        user = mc.user,
        password = mc.password,
        host = mc.host,
        database = mc.database
        )
        sql_drop = " DROP TABLE IF EXISTS {} ".format(tableName)
        sql_create_table = """CREATE TABLE {}( 
            username VARCHAR(255),
            date_taken VARCHAR(16),
            time_started VARCHAR(16),
            time_finished VARCHAR(16),
            answer_question_1 VARCHAR(255),
            answer_question_2 VARCHAR(255),
            answer_question_3 VARCHAR(255),
            answer_question_4 VARCHAR(255),
            answer_question_5 VARCHAR(255),
            answer_question_6 VARCHAR(255),
            PRIMARY KEY (username)
            )""".format(tableName)

        sql_insert_statement = """INSERT INTO {}( 
            username,
            date_taken,
            time_started,
            time_finished,
            answer_question_1,
            answer_question_2,
            answer_question_3,
            answer_question_4,
            answer_question_5,
            answer_question_6
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(tableName)
# Here we create a cursor, which we will use to execute
# the MySQL statements above. After each statement is executed,
# a message will be printed to the console if the execution was successful.
        cursor = connection.cursor()
        cursor.execute(sql_drop)
        print('Table {} has been dropped'.format(tableName))
        cursor.execute(sql_create_table)
        print('Table {} has been created'.format(tableName))
# We need to write each row of data to the table, so we use a for loop
# that will insert each row of data one at a time
        for i in sql_data:
            cursor.execute(sql_insert_statement, i)
# Now we execute the commit statement, and print to the console
# that the table was updated successfully
        connection.commit()
        print("Table {} successfully updated.".format(tableName))
# Errors are handled in the except block, and we will get
# the information printed to the console if there is an error
    except mysql.connector.Error as error :
        connection.rollback()
        print("Error: {}. Table {} not updated!".format(error, tableName))
# We need to close the cursor and the connection,
# and this needs to be done regardless of what happened above.
    finally:
        cursor.execute('SELECT COUNT(*) FROM {}'.format(tableName))
        rowCount = cursor.fetchone()[0]
        print(tableName, 'row count:', rowCount)
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")


# Replaces any empty cells with 'NULL'
def preserveNULLValues(listName):
    print('Preserving NULL values...')
    for x in range(len(listName)):
        for y in range(len(listName[x])):
            if listName[x][y] == '':
                listName[x][y] = None
    print('NULL values preserved.')

# Uses Google Drive's API.
# If you get an error regarding this, go to the link and enable it.
data = GetSpreadsheetData('rogoben', 0)

# Write to the table in the database.
preserveNULLValues(data)
WriteToMySQLTable(data, 'MyData')
