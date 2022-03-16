import mysql.connector

# cnx_obj = {'val': None}
cnx = None
DB_NAME = "db_pa_23456"

cnx = mysql.connector.connect(user='root', password='mysql',
                              host='localhost')