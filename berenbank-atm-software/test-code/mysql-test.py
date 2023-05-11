import mysql.connector
from mysql.connector import Error

try:
	connection = mysql.connector.connect(host='145.24.222.201',
										 database='testdb',
										 user='jpq',
										 password='qiu',
										 port='8008')
	
	query_uid = ("SELECT Card_UID FROM User")
	
	if connection.is_connected():
		db_info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_info)
		cursor = connection.cursor()
		cursor.execute("select database();")
		record = cursor.fetchone()
		print("You're connected to database: ", record)
					
except Error as e:
	print("Error while connecting to MySQL, e")
