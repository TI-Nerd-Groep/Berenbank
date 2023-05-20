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

connection = mysql.connector.connect(host='127.0.0.1',
                                    database='testdb',
                                    user='pacy',
                                    password='qiu8',
                                    port='8008')

@sio.event
def connect():
    print("I'm connected! ")

    try:

        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL, e")

@sio.on("UID")
def get_customer_name(UID):
    cursor = connection.cursor()
    cursor.execute(get_name, (UID,))
    
    global first_name
    global last_name
    global customer_UID
    
    customer_UID = UID
    
    for (firstName, lastName) in cursor:
        first_name = firstName
        last_name = lastName
        
        print(first_name)
        print(last_name)
    
    cursor.close()

@sio.on("pin")
def get_pin_code(pin):
    cursor = connection.cursor()
    cursor.execute(get_pin, (customer_UID,))

    pin = int(pin)
    
    for (pincode,) in cursor:
        correct_pin = pincode
    
    if pin == correct_pin:
        print("Correct pin")
    else:
        print("Incorrect pin")
    print(correct_pin)
    print(pin)
    
# Fill in generated url from ngrok. 
sio.connect("https://cc3f-45-84-40-171.ngrok-free.app")

