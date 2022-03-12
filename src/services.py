import mysql.connector
cnx = mysql.connector.connect(user='root', password='mysql',
                              host='127.0.0.1')

DB_NAME = "db_pa_2"

def try_log_in(username, password):
  cursor = cnx.cursor()

  cursor.execute(f"""
    USE {DB_NAME};
  """)

  cursor.execute("""
    SELECT id FROM user WHERE username = %s AND password = %s LIMIT 1;
  """, (username, password))

  result = cursor.fetchone()

  # WIP