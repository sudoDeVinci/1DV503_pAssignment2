import mysql.connector

cnx = None
DB_NAME = "db_pa_2"

cnx = mysql.connector.connect(user='root', password='root',
                              host='localhost')