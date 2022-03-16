import mysql.connector
from services import insert_account, insert_brand, insert_category, insert_product
from db_conn import cnx, DB_NAME


def init_db():
    cursor = cnx.cursor()

    cursor.execute(f"""
        CREATE DATABASE {DB_NAME};
    """)

    cnx.database = DB_NAME

    cursor.execute("""
        CREATE TABLE brand (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT now(),

            PRIMARY KEY (id)
        ); 
    """)

    cursor.execute("""
        CREATE TABLE category (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            created_at TIMESTAMP default now(),

            PRIMARY KEY (id)
        ); 
    """)

    cursor.execute("""
        CREATE TABLE product (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(50) NOT NULL,
            description TEXT NOT NULL,
            price DECIMAL(8,2) NOT NULL,
            created_at TIMESTAMP default now(),

            category_id INT NOT NULL,
            brand_id INT NOT NULL,

            PRIMARY KEY (id),
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (brand_id) REFERENCES brand(id)
        ); 
    """)

    cursor.execute("""
        CREATE TABLE category_closure (
            ancestor_id INT NOT NULL,
            descendant_id INT NOT NULL,
            depth INT(2),

            PRIMARY KEY (ancestor_id,descendant_id),
            INDEX (descendant_id),
            FOREIGN KEY (ancestor_id) REFERENCES category(id),
            FOREIGN KEY (descendant_id) REFERENCES category(id)
        ); 
    """)

    cursor.execute("""
        CREATE TABLE user (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            role ENUM('user', 'admin'),

            PRIMARY KEY (id)
        ); 
    """)

    cursor.execute("""
        CREATE OR REPLACE VIEW productCategoryAncestryLine AS
        SELECT p.*, GROUP_CONCAT(c.name ORDER BY depth DESC SEPARATOR " -> ") categories FROM product p
        INNER JOIN category_closure cc ON cc.descendant_id = p.category_id
        INNER JOIN category c ON c.id = cc.ancestor_id
        GROUP BY p.id
    """)

    cnx.commit()

    insert_account('admin', 'admin', 'admin')
    insert_account('user', 'user', 'user')

    _cid1 = insert_category('Electronics', None)
    _cid2 = insert_category('Computers', _cid1)
    _cid3 = insert_category('Laptops', _cid2)
    _cid4 = insert_category('Ultrabooks', _cid3)
    _cid5 = insert_category('Desktops', _cid2)
    _cid6 = insert_category('Smartphones', _cid1)
    _cid7 = insert_category('Kitchenware', None)
    _cid8 = insert_category('Utensils', _cid7)
    _cid9 = insert_category('Clothing', None)
    _cid10 = insert_category('Men\'s Clothing', _cid9)
    _cid11 = insert_category('Women\'s Clothing', _cid9)
    _cid12 = insert_category('PC Components', _cid2)
    _cid13 = insert_category('Food storage', _cid8)

    _bid = insert_brand('Dell')
    insert_product('Optiplex Ultrabook', 'It\'s an ultrabook.', 1100, _cid4, _bid)
    insert_product('Optiplex 750', 'It\'s a legend.', 1000, _cid5, _bid)
    insert_product('Optiplex Tower', 'Huge boi.', 2000, _cid5, _bid)

    _bid = insert_brand('Asus')
    insert_product('Light', 'Zero sugar.', 3000, _cid4, _bid)
    insert_product('TufBook Gaming', 'As tough as a gamer.', 3200, _cid4, _bid)
    insert_product('ROG Strix B450 Motherboard x12', 'Ye olde motherboard', 4500, _cid12, _bid)

    _bid = insert_brand('Samsung')
    insert_product('Galaxy Note 10', 'Big phone. Beware.', 3000, _cid6, _bid)
    insert_product('Galaxy S20', 'A flagship phone', 4000, _cid6, _bid)
    insert_product('Galaxy S21 Ultra', 'Yet another flagship phone', 5500, _cid6, _bid)

    _bid = insert_brand('Deiss')
    insert_product('Parmigiano Regiano Grater',
                   'Grates parmigiano regiano. What else would it do?', 100, _cid8, _bid)
    insert_product('Stainless Steel Spatula',
                   'It\'s a spatula.', 70, _cid8, _bid)
    insert_product('Stainless Steel Knife set',
                   'For cutting food, not people', 275, _cid8, _bid)

    _bid = insert_brand('Emprio Armani')
    insert_product('Men\'s shirt', 'What did you expect?', 5000, _cid10, _bid)
    insert_product('Men\'s dress pants',
                   'Dress pants... for men.', 5500, _cid10, _bid)
    insert_product('Women\'s shirt', 'It\'s a shirt. What did you expect?',
                   5000, _cid11, _bid)
    insert_product('Women\'s dress pants',
                   'Exactly what you would expect...', 5500, _cid11, _bid)


def check_db_exists():
    cursor = cnx.cursor()

    cursor.execute(f"""
        SHOW DATABASES LIKE '{DB_NAME}';
    """)

    return bool(len(cursor.fetchall()))


def DB_connect():
    if not check_db_exists():
        print("Database does not exist, initialializing ... ")
        init_db()
    else:
        cnx.database = DB_NAME
