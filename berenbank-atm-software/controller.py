import smbus
import time
import mysql.connector
from mysql.connector import Error

query_last_name = ("SELECT lastName FROM User "
                    "WHERE Card_UID = %s")

try:
	connection = mysql.connector.connect(host='145.24.222.201',
										 database='testdb',
										 user='jpq',
										 password='qiu',
										 port='8008')
	
	if connection.is_connected():
		db_info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_info)
		cursor = connection.cursor()
		cursor.execute("select database();")
		record = cursor.fetchone()
		print("You're connected to database: ", record)
					
except Error as e:
	print("Error while connecting to MySQL, e")

bus = smbus.SMBus(1)
address = 0x2a

while True:
    data = ""
    
    for i in range(0, 11):
        data += chr(bus.read_byte(address));
    print(data)
    
    cursor.execute(query_last_name, (data,))
    for (info) in cursor:
        print("Last Name: {}".format(info))
    time.sleep(1);


