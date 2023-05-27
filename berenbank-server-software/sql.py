import mysql.connector
from mysql.connector import Error
import socketio
import requests

http_session = requests.Session()
http_session.verify = False

sio = socketio.Client(http_session = http_session)

# Queries
get_id = ("SELECT id FROM User "
          "WHERE Card_UID = %s")

get_name = ("SELECT firstName, lastName FROM User "
            "WHERE Card_UID = %s")

get_pin = ("SELECT Pincode FROM User "
           "WHERE Card_UID = %s")

get_balance = ("SELECT balance FROM User "
               "WHERE Card_UID = %s")

get_blocked = ("SELECT isBlocked FROM User "
               "WHERE Card_UID = %s")

withdraw = ("UPDATE User "
            "SET balance = balance - %d "
            "WHERE Card_UID = %s")

set_blocked = ("UPDATE User SET isBlocked = TRUE "
               "WHERE Card_UID = %s")

set_unblocked = ("UPDATE User SET isBlocked = FALSE "
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
        
# Auth events
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
        sio.emit("page_data", 1)
        sio.emit("correct_pin")
    else:
        print("Incorrect pin")
        sio.emit("page_data", 0)
        
    print(correct_pin)
    print(pin)

    cursor.close()
    
@sio.on("balance")
def get_amount():
    cursor = connection.cursor()
    cursor.execute(get_balance, (customer_UID,))
    
    for (balance,) in cursor:
        user_balance = str(balance)
        
    print(user_balance)
    sio.emit("page_data_balance", user_balance)
    
    cursor.close()

@sio.on("blocked")
def get_block_status():
    cursor = connection.cursor()
    cursor.execute(get_blocked, (customer_UID,))
    
    for (isBlocked,) in cursor:
        block_status = isBlocked

    cursor.close()
    cursor = connection.cursor()
    
    sio.emit("block_message")
    cursor.execute(set_blocked, (customer_UID,))
    connection.commit()
    cursor.close()
    print(block_status)
    
# Fill in generated url from ngrok. 
sio.connect("https://d053-45-84-40-165.ngrok-free.app")

