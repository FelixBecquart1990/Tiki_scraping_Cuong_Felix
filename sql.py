import psycopg2


conn = psycopg2.connect(user="felix", database="tiki", password="felixpostgre")
conn.autocommit = True
cursor = conn.cursor()


numberOfCategoriesShown = 5
iDselectedCategory = 228


def get_categories(numberOfCategoriesToAdd):
    global numberOfCategoriesShown
    cursor.execute("SELECT * FROM categories LIMIT " +
                   str(numberOfCategoriesShown + numberOfCategoriesToAdd))
    categories = cursor.fetchall()
    numberOfCategoriesShown += numberOfCategoriesToAdd
    return categories


def get_category():
    global iDselectedCategory
    cursor.execute("SELECT * FROM categories WHERE id=" +
                   str(iDselectedCategory))
    category = cursor.fetchall()
    return category[0]


def get_number_of_categories():
    cursor.execute("SELECT COUNT(*) FROM categories")
    numberOfCategories = cursor.fetchall()
    return numberOfCategories

    
# import the data from the JSON file
# insert_query = "INSERT INTO student VALUES {}".format("(4, 'felix', 'hello@dataquest.io')")
# cur.execute(insert_query)
# conn.commit()

  # categories = []
  # import psycopg2
  # conn = psycopg2.connect("dbname=tiki user=felix password=felixpostgre")
  # cur = conn.cursor()
  # cur.execute('SELECT * FROM categories')
  # categories = cur.fetchall()
  # conn.close()
