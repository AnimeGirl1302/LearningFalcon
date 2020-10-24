import os
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', 
                                passwd='#insanegirl123', database='ComplaintBox',
                                auth_plugin='mysql_native_password')

mycursor = mydb.cursor()

# mycursor.execute("USE ComplaintBox")

#CREATE TABLE user (mobile CHAR(10) PRIMARY KEY, name VARCHAR(20), city VARCHAR(20))")

#CREATE TABLE complaint (comp_id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(20), descrip VARCHAR(255), mobile CHAR(10) REFERENCES user(mobile))"

#CREATE TABLE complaint_status (status VARCHAR(20), comp_id INT REFERENCES complaint(comp_id))"

# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#     print(x)

# mydb.commit()