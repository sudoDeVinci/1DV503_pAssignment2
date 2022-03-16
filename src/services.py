from typing import List
import mysql.connector
import uuid
from db_conn import cnx


def log_in(username, password):
    """
    Finds a user with the given username and password
    and returns a dict with the user's role.

    If credentials are incorrect, returns None.

    This is not meant to be secure. Do not try this at home.
    """

    cursor = cnx.cursor(dictionary=True)

    # HASHING WOULD OCCUR HERE

    cursor.execute("""
        SELECT role FROM user WHERE username = %s AND password = %s LIMIT 1;
    """, (username, password))

    result = cursor.fetchone()

    return result


def print_category_tree():
    """
    Returns a tree of all the categories.
    """

    cursor = cnx.cursor(dictionary=True)

    # This query returns all the categories as well as the id of their parent category (or NULL).
    # This works by joining all categories with the closure table using only the rows that have depth = 1,
    # which means the ancestor is the direct parent.
    # The depth condition has to be under ON and not WHERE so that the LEFT JOIN will include NULL values for top-level categories.
    cursor.execute("""
        SELECT c.*, cc.ancestor_id, cc.depth FROM category c
        LEFT JOIN category_closure cc ON cc.descendant_id = c.id AND cc.depth = 1;
    """)

    categories: List = cursor.fetchall()

    # simple iteration to create a tree structure out of the results
    for category in categories:
        if category['ancestor_id'] is not None:
            ancestor = next(
                x for x in categories if x['id'] == category['ancestor_id'])
            if ancestor is not None:
                if 'children' not in ancestor:
                    ancestor['children'] = []

                ancestor['children'].append(category)

    # roots = top-level categories = categories without a parent
    roots = [c for c in categories if c['ancestor_id'] is None]

    # prints cool tree from a root
    def print_tree(node, depth=0):
        text_gizmo = '│  ' * (depth - 1) + '└─ ' if depth > 0 else ''
        print((str(node['id'])).rjust(4) + ' ' + text_gizmo + node['name'])
        if 'children' in node:
            for child in node['children']:
                print_tree(child, depth + 1)

    print('  id name')
    print('──── ────')
    for root in roots:
        print_tree(root)


def insert_category(name, parent):
    cursor = cnx.cursor(named_tuple=True)

    # First simply add the category to the category table
    cursor.execute("""
        INSERT INTO category (name)
        VALUES (%s);
    """, [name])

    # Get its id (wow mysql sucks)
    cursor.execute("""
        SELECT LAST_INSERT_ID() as last_id;
    """)

    _id = cursor.fetchone().last_id

    # Then, add that category node into the category tree
    # -- in this case, add links from the node to all its ancestors
    #
    # This query works by getting all the links where `parent` is the descendant,
    # and using the ancestors for the newly inserted links,
    # since every node will need to have links for every ancestor above it.
    # Also inserts a self-referencing link of depth 0.
    cursor.execute("""
        INSERT INTO category_closure (ancestor_id, descendant_id, depth)
        SELECT ancestor_id, %s, depth+1
        FROM category_closure
        WHERE descendant_id = %s
        UNION ALL SELECT %s, %s, 0
    """, [_id, parent, _id, _id])

    cnx.commit()

    return _id


def print_brands():
    """
    Prints all the brands.
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        SELECT * FROM brand ORDER BY created_at;
    """)

    results = cursor.fetchall()

    for row in results:
        print(row.name)


def insert_brand(name):
    """
    Inserts a brand with a given name.
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        INSERT INTO brand (name)
        VALUES (%s);
    """, [name])

    cursor.execute("""
        SELECT LAST_INSERT_ID() as last_id;
    """)

    _id = cursor.fetchone().last_id

    cnx.commit()

    return _id


def insert_account(username, password, role):
    """
    Inserts a brand with a given username, password, and role.

    This is not meant to be secure. Do not try this at home.
    """

    cursor = cnx.cursor(named_tuple=True)

    # HASHING WOULD OCCUR HERE

    cursor.execute("""
        INSERT INTO user (username, password, role)
        VALUES (%s, %s, %s);
    """, [username, password, role])

    cnx.commit()


def print_products_of_brand(brand):
    """
    Prints all the products of a given brand.
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        SELECT p.*, b.name brand_name FROM productCategoryAncestryLine p
        INNER JOIN brand b ON b.id = p.brand_id
        WHERE brand_id = %s
        ORDER BY created_at;
    """, [brand])

    results = cursor.fetchall()

    for row in results:
        print(
            f"\n{row.brand_name} {row.name}"
            + f"\ncategories: {row.categories}"
            + f"\ndescription: {row.description}"
            + f"\nprice: {row.price}"
        )


def get_brand_id_from_name(brand_name):
    """
    Given the brand name, returns its id.
    """
    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        SELECT id FROM brand b
        WHERE name = %s
        LIMIT 1;
    """, [brand_name])

    return cursor.fetchone().id


def insert_product(name, description, price, category_id, brand_id):
    """
    Inserts a product with the given data.
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        INSERT INTO product (name, description, price, category_id, brand_id)
        VALUES (%s, %s, %s, %s, %s);
    """, [name, description, price, category_id, brand_id])

    cnx.commit()

# def get_stats_for_brands(brand):
    # cursor = cnx.cursor(named_tuple=True)

    # cursor.execute("""
    #   SELECT AVG(p.price) avg_price, COUNT(*) count, b.name brand_name FROM product p
    #   INNER JOIN brand b ON b.id = p.brand_id
    #   WHERE brand_id = %s;
    # """, [brand])

    # results = cursor.fetchall()

    # for row in results:
    #   print(
    #     row.name
    #     + f"\ndescription{row.description}"
    #   )


def get_price_range_stats():
    """
    Prints how many products there are in every price range
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        SELECT FLOOR(p.price / 100) * 100 price_range, COUNT(*) count FROM product p
        GROUP BY price_range ORDER BY price_range
    """)

    results = cursor.fetchall()

    largest = max([len(str(x.price_range)) for x in results])

    for row in results:
        print(f"${row.price_range}-{row.price_range+100}:".rjust(largest *
              2 + 3) + ' ' + f"{row.count} product(s)")


def get_products_by_partial_name(name):
    """
    Search products by partial name string
    """

    cursor = cnx.cursor(named_tuple=True)

    cursor.execute("""
        SELECT p.*, b.name brand_name FROM productCategoryAncestryLine p
        INNER JOIN brand b ON b.id = p.brand_id
        WHERE concat(b.name, " ", p.name) LIKE %s;
    """, ['%' + name + '%'])

    results = cursor.fetchall()
    return results
