from django.db import models
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd ="123456", database="db-hotel")

mycursor = mydb.cursor()

mycursor.execute("Show tables")

