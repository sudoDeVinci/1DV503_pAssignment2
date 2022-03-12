import mysql.connector

def init_db():
  cnx = mysql.connector.connect(user='root', password='mysql',
                                host='127.0.0.1')

  DB_NAME = "db_pa_2"

  cursor = cnx.cursor()

  cursor.execute(f"""
    CREATE DATABASE {DB_NAME};
  """)

  cursor.execute(f"""
    USE {DB_NAME};
  """)

  cursor.execute("""
    CREATE TABLE brand (
      id VARCHAR(36) NOT NULL,
      name VARCHAR(50) NOT NULL,
      created_at TIMESTAMP default now(),

      PRIMARY KEY (id)
    ); 
  """)

  cursor.execute("""
    CREATE TABLE category (
      id VARCHAR(36) NOT NULL,
      name VARCHAR(50) NOT NULL,
      created_at TIMESTAMP default now(),

      PRIMARY KEY (id)
    ); 
  """)

  cursor.execute("""
    CREATE TABLE product (
      id VARCHAR(36) NOT NULL,
      name VARCHAR(50) NOT NULL,
      description TEXT NOT NULL,
      price DECIMAL(5,2) NOT NULL,
      created_at TIMESTAMP default now(),

      category_id VARCHAR(36) NOT NULL,
      brand_id VARCHAR(36) NOT NULL,

      PRIMARY KEY (id),
      FOREIGN KEY (category_id) REFERENCES category(id),
      FOREIGN KEY (brand_id) REFERENCES brand(id)
    ); 
  """)

  cursor.execute("""
    CREATE TABLE category_closure (
      ancestor_id VARCHAR(36) NOT NULL,
      descendant_id VARCHAR(36) NOT NULL,
      depth INT(2),

      PRIMARY KEY (ancestor_id,descendant_id),
      INDEX (descendant_id),
      FOREIGN KEY (ancestor_id) REFERENCES category(id),
      FOREIGN KEY (descendant_id) REFERENCES category(id)
    ); 
  """)

  cursor.execute("""
    CREATE TABLE user (
      id VARCHAR(36) NOT NULL,
      username VARCHAR(50) NOT NULL,
      password VARCHAR(50) NOT NULL,

      PRIMARY KEY (id)
    ); 
  """)

init_db()
