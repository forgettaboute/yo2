import mysql.connector
from mysql.connector import Error

def createConnection(hostname, username, password, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            passwd = password,
            database = dbname
        )
        print("Successfully connected to MySQL Database!")
    except Error as e:
        print(f"The error '{e}' occurred :(")
    
    return connection

def executeReadQuery(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred :(")

def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return ("Query successfully executed!")
    except Error as e:
        return f"(The error '{e}' has occurred :("
