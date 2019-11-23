import psycopg2
from bs4 import BeautifulSoup
import requests
from collections import deque

TIKI_URL = 'https://tiki.vn/'

conn = psycopg2.connect(user="felix", database="tiki", password="felixpostgre")
conn.autocommit = True
cursor = conn.cursor()


def create_categories_table():
    query = """
        CREATE TABLE IF NOT EXISTS categories(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            url TEXT,
            parent_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
    """
    try:
        cursor.execute(query)
        crawl_main_categories(True)
    except Exception as err:
        print(f'ERROR: {err}')

def create_products_table():
    query = """
        CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            url TEXT,
            parent_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
    """
    try:
        cursor.execute(query)
        crawl_main_categories(True)
    except Exception as err:
        print(f'ERROR: {err}')

def crawl_main_categories(save_db=False):
    s = parse(TIKI_URL)
    category_list = []
    # Scrape through the navigator bar on Tiki homepage
    for i in s.findAll('a', {'class': 'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
        # new category has no id
        cat_id = None
        # Get the category name
        name = i.find('span', {'class': 'text'}).text
        # Get the url value
        url = i['href'] + "&page=1"
        # main categories has no parent
        parent_id = None

        # Add category and url values to list
        cat = Category(None, name, url, parent_id)
        if save_db:
            cat.save_into_db()
        category_list.append(cat)

    return category_list


class Category:
    def __init__(self, cat_id, name, url, parent_id):
        self.cat_id = cat_id
        self.name = name
        self.url = url
        self.parent_id = parent_id

    def save_into_db(self):

        query = 'SELECT url FROM categories WHERE url LIKE %s;'
        val = (self.url,)
        try:
            cursor.execute(query, val)
            result = cursor.fetchall()
            if len(result) > 0:
                return ''
        except Exception as err:
            print(f'ERROR: {err}')

        query = f"""
            INSERT INTO categories (name, url, parent_id) 
            VALUES (%s, %s, %s) RETURNING id;
        """
        val = (self.name, self.url, self.parent_id)
        print(
            f'ID: {self.cat_id}, Parent ID: {self.parent_id}')
        try:
            cursor.execute(query, val)
            # Get id of the new row
            self.cat_id = cursor.fetchone()[0]
        except Exception as err:
            print(f'ERROR: {err}')

    def __repr__(self):
        return f'ID: {self.cat_id}, Name: {self.name}, URL: {self.url}, Parent ID: {self.parent_id}'


def parse(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, "html.parser")
        return response
    except Exception as err:
        print(f'ERROR: {err}')
        return ''


def crawl_sub_categories(category, save_db=False):
    name = category.name
    url = category.url
    sub_categories = []

    try:
        div_containers = parse(url).find_all(
            'div', attrs={"class": "list-group-item is-child"})
        for div in div_containers:
            sub_id = None
            sub_name = div.a.text
            sub_url = 'https://tiki.vn' + div.a.get('href')
            sub_parent_id = category.cat_id

            cat = Category(sub_id, sub_name, sub_url, sub_parent_id)
            if save_db:
                cat.save_into_db()
            if cat.cat_id is not None:
                sub_categories.append(cat)
    except Exception as err:
        print(f'ERROR: {err}')

    return sub_categories


def crawl_all_subcategories(main_categories):
    queue = deque(main_categories)
    count = 0
    while queue:
        parent_cat = queue.popleft()
        sub_list = crawl_sub_categories(parent_cat, save_db=True)
        queue.extend(sub_list)

        # sub_list is empty, which mean the parent_cat has no sub-categories
        if not sub_list:
            count += 1
            if count % 100 == 0:
                print(f'{count} number of deepest nodes')


numberOfMainCategoriesShown = 10
iDselectedCategory = 32


def get_main_categories(numberOfMainCategoriesToAdd):
    # def get_main_categories():
    global numberOfMainCategoriesShown
    cursor.execute("SELECT * FROM categories WHERE parent_id IS NULL LIMIT " +
                   str(numberOfMainCategoriesShown + numberOfMainCategoriesToAdd))
    mainCategories = cursor.fetchall()
    numberOfMainCategoriesShown += numberOfMainCategoriesToAdd
    return mainCategories


def get_category():
    global iDselectedCategory
    cursor.execute("SELECT * FROM categories WHERE id=" +
                   str(iDselectedCategory))
    category = cursor.fetchall()
    return category[0]


def get_subcategories():
    global iDselectedCategory
    cursor.execute("SELECT * FROM categories WHERE parent_id=" +
                   str(iDselectedCategory))
    # cursor.execute("SELECT * FROM categories LIMIT 15 OFFSET 200")
    subcategories = cursor.fetchall()
    return subcategories


def get_number_of_main_categories():
    cursor.execute("SELECT COUNT(*) FROM categories WHERE parent_id IS NULL")
    numberOfMainCategories = cursor.fetchall()
    return numberOfMainCategories


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
