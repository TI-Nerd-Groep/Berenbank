import mysql.connector
from mysql.connector import Error
import socketio

sio = socketio.Client()

# Queries
get_id = ("SELECT id FROM User "
          "WHERE Card_UID = %s")

get_name = ("SELECT firstName, lastName FROM User "
            "WHERE Card_UID = %s")

get_pin = ("SELECT Pincode FROM User "
           "WHERE Card_UID = %s")

try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='testdb',
                                         user='pacy',
                                         password='qiu8',
                                         port='8008')

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

    cursor = connection.cursor()
    cursor.execute(get_name, ("8E E8 1F 02",))
    
    for (firstName, lastName) in cursor:
        first_name = firstName
        last_name = lastName
        
        print(first_name)
        print(last_name)
    
    cursor.close()

except Error as e:
    print("Error while connecting to MySQL, e")


