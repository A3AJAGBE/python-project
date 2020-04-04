import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'raise_on_warnings': True,
}

link = mysql.connector.connect(**config)

mycursor = link.cursor()

"""
#test creating a database

mycursor.execute("CREATE DATABASE testS")

"""

"""
#Showing all database

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)
"""
mycursor.execute("CREATE DATABASE DrugSystem")

link.close()
