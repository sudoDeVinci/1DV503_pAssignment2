import services
from db_conn import cnx, DB_NAME
from init import DB_connect

# Login Screen  -- Check role
def get_role():
    print("\nWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n--------- LOGIN ---------\n")
    username = input("\033[1m username : \033[0m").strip()
    password = input("\033[1m password : \033[0m").strip()
    role = services.log_in(username, password)
    # print(role['role'])
    if role == None:
        ret_role = None
    else:
        ret_role = role['role']

    # If user not found, exit with no error
    while ret_role is None:
        print("\n\033[91mUser not found. Please check details and try again.\033[0m \n")
        username = input("\033[1m username : \033[0m").strip()
        password = input("\033[1m password : \033[0m").strip()
        role = services.log_in(username, password)
        if role == None:
            ret_role = None
        else:
            ret_role = role['role']
    
    return ret_role


# Print categories (Including Admin options)
def print_categories():
    print("\n------ CATEGORIES ------\n")
    services.print_category_tree()
    print("\n------------------------")


# Print Brands
def print_brands():
    print("\n------ BRANDS ------\n")
    services.print_brands()
    print("\n--------------------")


# Insert categories (Specify if top-level via args)
def insert_category():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[93mTo insert a category, specify the name and parent id below.
Leave parent category blank if none applies.\033[0m \n""")
    category = input("\033[1mNew Category : \033[0m").strip()
    parent = input("\033[1mParent Category ID : \033[0m").strip()

    if category == '':
        category = None
    if parent == '':
        parent = None

    try:
        services.insert_category(category, parent)
    except Exception as e:
        print("\n\033[91mPlease check category data and retry\033[0m \n")
        print(e)
    print("\n------------------------------------------------------------------")


# Insert products(Specify brand and category)
def insert_product():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[93m To insert a product, specify the brand, product name, category ID, price and description. \033[0m \n""")
    brand = input("\033[1mBrand : \033[0m").strip()
    name = input("\033[1mName : \033[0m").strip()
    category_id = input("\033[1mCategory ID: \033[0m").strip()
    price = input("\033[1mPrice : \033[0m").strip()
    description = input("\033[1mDescription : \033[0m").strip()

    if category_id == '':
        category_id = None
    if brand == '':
        brand = None
    if name == '':
        name = None
    if price == '':
        price = None
    if description == '':
        description = None

    try:
        brand_id = services.get_brand_id_from_name(brand)
        services.insert_product(name, description, price, category_id, brand_id)
    except Exception as e:
        print("\n\033[91mPlease check product data and retry\033[0m \n")
        print(e)
    print("\n------------------------------------------------------------------")


# Print Products of given brands
def print_products_of_brand():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[93m To print products of a specific brand, please specify the name below.\033[0m \n""")
    brand = input("\033[1mBrand Name : \033[0m").strip()

    if brand == '':
        brand = None
        return None
    try:
        brand_id = services.get_brand_id_from_name(brand)
        services.print_products_of_brand(brand_id)
    except Exception as e:
        print("\n\033[91mPlease check brand name and retry\033[0m \n")
        print(e)
    print("\n------------------------------------------------------------------")


# Insert Brand (brandname)
def insert_brand():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[93m To insert a brand, specify the brand name.\033[0m \n""")
    brand = input("\033[1mBrand Name : \033[0m").strip()

    if brand == '':
        brand = None

    try:
        services.insert_brand(brand)
    except Exception as e:
        print("\n\033[91mPlease check brand name and retry\033[0m \n")
        print(e)
    print("\n------------------------------------------------------------------") 


# Admin account creation (specify permission level)
def create_account():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[0;34m To create a new user account, specify the credentials and role below.\033[0m \n""")
    username = input("\033[1mUsername : \033[0m").strip()
    while username == '' or username == None or username == "None":
        print("\033[0;31m\nInvalid Username, Retry.\033[0m")
        username = input("\n\033[1mUsername : \033[0m").strip()


    matched = False
    while matched == False:
        password_1 = input("\033[1mPassword : \033[0m").strip()
        password_2 = input("\033[1mEnter again : \033[0m").strip()
        if password_1 == password_2:
            if password_1 != '':
                matched = True
                break
            else:
                print("\033[0;31m\nPassword cannot be blank.\033[0m")
        else:
            print("\033[0;31m\nPasswords do not macth. Retry.\033[0m")


    role = input("\033[1mAccount Role : \033[0m").strip().lower()

    while role != "admin" and role != "user":
        print(f"\033[0;31m\nInvalid role '{role}'. \nValid roles are" + " \033[0;33m'admin' " + "\033[0;31mand" + " \033[0;33m'user'\033[0;31m.\033[0m")
        role = input("\033[1mAccount Role : \033[0m").strip().lower()


    try:
        services.insert_account(username, password_1, role)
        print(f"\n\033[0;32m{role} account {username} created successfully.\033[0m \n")
    except Exception as e:
        print("\n\033[91mPlease check credentials name and retry\033[0m \n")
        print(e)
    print("\n------------------------------------------------------------------") 


# Print products by partial name
def partial_name_search():
    print("\n------------------------------------------------------------------")
    print("""\033[1m\033[0;34mTo search for a product by its name, enter it below.\033[0m \n""")
    product = input("\033[1mSearch : \033[0m").strip()

    while product == '' or product == None or product == "None":
        print("\033[0;31m\nSearch can't be empty or None.\033[0m")
        product = input("\033[1mSearch : \033[0m").strip()
    
    try:
        results = services.get_products_by_partial_name(product)
    except Exception as e:
        print("\n\033[91mPlease check search term and try again.\033[0m \n")
        print(e)
        return 0

    if len(results) == 0:
        color = "\033[0;31m"
    else:
        color = "\033[0;36m"
    print(f"\n{color}{len(results)} products found with \"{product}\" \033[0m")
    for row in results:
        print(
        f"\n{row.brand_name} {row.name}"
        + f"\ncategories: {row.categories}"
        + f"\ndescription: {row.description}"
        + f"\nprice: {row.price}"
        )
    
    print("\n------------------------------------------------------------------")


# Get Price range stats
def price_range_stats():
    print("\n------ PRICE RANGE STATS ------\n")
    services.get_price_range_stats()
    print("\n-------------------------------")


def main():
    DB_connect()

    role = get_role()

    print_categories()
    while True:
        print("\033[93m\nPlease select one of the below options: \033[0m\n")

        if role == "admin":
            # Printout for admins
            print("""[1] Display Categories\n[2] Display Brands\n[3] Display Products of Brand\n[4] Add Product\n[5] Add Brand\n[6] Add Category\n[7] Product Search\n[8] Add Account (admin only)\n[9] Price Range Stats\n[10] Exit""")

        else:
            # Printout for users has option 9 greyed out
            print("[1] Display Categories\n[2] Display Brands\n[3] Display Products of Brand\n[4] Add Product\n[5] Add Brand\n[6] Add Category\n[7] Product Search" + "+\n\033[1;30m[8] Add Account (admin only)\033[0m" + "\n[9] Price Range Stats\n[10] Exit")

        choice = input("\n\033[0;36m> \033[0m").strip()

        # Display categories
        if choice == "1":
            print_categories()

        # Display Brands
        elif choice == "2":
            print_brands()

        # Display products of Brand
        elif choice == "3":
            print_products_of_brand()

        # Add Product
        elif choice == "4":
            insert_product()

        # Add Brand
        elif choice == "5":
            insert_brand()

        # Add Category
        elif choice == "6":
            insert_category()

        # Product Search
        elif choice == "7":
            partial_name_search()
        
        # Add Account
        elif choice == "8":
            if role == "admin":
                create_account()
            else:
                print("\n\033[91mOnly admins can use this feature.\033[0m \n")
        
        # Price Range stats
        elif choice == "9":
            price_range_stats()

        # Exit
        elif choice == "10":
            break

        else:
            print("\n\033[91mInavlid Selection.\033[0m \n")
            

    print("\nSee You Later (⌐ ͡■ ͜ʖ ͡■) \n\n--------- EXIT ---------\n")


main()