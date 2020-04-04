import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'raise_on_warnings': True,
  'database': 'DrugSystem'
}

link = mysql.connector.connect(**config)

mycursor = link.cursor()
mycursor.execute("CREATE TABLE LoginAccess (LoginAccess_Id INT NOT NULL AUTO_INCREMENT, Name VARCHAR(255) NOT NULL, Username VARCHAR(255) NOT NULL, Email VARCHAR(100) NOT NULL, CONSTRAINT PK_LoginAccess PRIMARY KEY(LoginAccess_Id))");

link.close()
