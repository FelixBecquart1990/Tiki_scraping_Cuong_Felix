import psycopg2
from bs4 import BeautifulSoup
import requests
from collections import deque

TIKI_URL = 'https://tiki.vn/'

conn = psycopg2.connect(user="felix", database="tiki", password="felixpostgre")
conn.autocommit = True
cursor = conn.cursor()


def create_products_table():
    query = """
        CREATE TABLE IF NOT EXISTS products(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
    """
    try:
        cursor.execute(query)
        # crawl_main_categories(True)
    except Exception as err:
        print(f'ERROR: {err}')

# def crawl_main_categories(save_db=False):
#     s = parse(TIKI_URL)
#     category_list = []
#     # Scrape through the navigator bar on Tiki homepage
#     for i in s.findAll('a', {'class': 'MenuItem__MenuLink-tii3xq-1 efuIbv'}):
#         # new category has no id
#         cat_id = None
#         # Get the category name
#         name = i.find('span', {'class': 'text'}).text
#         # Get the url value
#         url = i['href'] + "&page=1"
#         # main categories has no parent
#         parent_id = None

#         # Add category and url values to list
#         cat = Category(None, name, url, parent_id)
#         if save_db:
#             cat.save_into_db()
#         category_list.append(cat)

#     return category_list


class Product:
    def __init__(self, title, image):
        self.title = title
        self.image = image

    def save_into_db(self):

        # query = 'SELECT url FROM products WHERE url LIKE %s;'
        # val = (self.url,)
        # try:
        #     cursor.execute(query, val)
        #     result = cursor.fetchall()
        #     if len(result) > 0:
        #         return ''
        # except Exception as err:
        #     print(f'ERROR: {err}')

        query = f"""
            INSERT INTO products (title, image) 
            VALUES (%s, %s) RETURNING id;
        """
        val = (self.title, self.image)
        print(
            f'title: {self.title}')
        try:
            cursor.execute(query, val)
            # Get id of the new row
            # self.product_id = cursor.fetchone()[0]
        except Exception as err:
            print(f'ERROR: {err}')

    def __repr__(self):
        return f'ID: {self.product_id}, Name: {self.title}'


def parse(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, "html.parser")
        return response
    except Exception as err:
        print(f'ERROR: {err}')
        return ''


def crawl_products(url, save_db=False):
    # title = product.title
    # image = product.image
    url = url

    try:
        div_containers = parse(url).find_all(
            'div', attrs={"class": "product-item"})
        print(div_containers)
        if div_containers == []:
            return "no more products"
        for div in div_containers:
            title = div.get('data-title')
            image = div.img['src']
            product = Product(title, image)
            if save_db:
                product.save_into_db()
    except Exception as err:
        print(f'ERROR: {err}')

    return print("end of page crawling")


def crawl_all_products_of_a_category(save_db=False):
    url = 'https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner&page='
    i = 1
    while crawl_products(url+str(i), True) != "no more products":
        i += 1

# def crawl_all_subcategories(main_categories):
#     queue = deque(main_categories)
#     count = 0
#     while queue:
#         parent_cat = queue.popleft()
#         sub_list = crawl_sub_categories(parent_cat, save_db=True)
#         queue.extend(sub_list)

#         # sub_list is empty, which mean the parent_cat has no sub-categories
#         if not sub_list:
#             count += 1
#             if count % 100 == 0:
#                 print(f'{count} number of deepest nodes')


# numberOfMainCategoriesShown = 10
# iDselectedCategory = 32


# def get_main_categories(numberOfMainCategoriesToAdd):
#     # def get_main_categories():
#     global numberOfMainCategoriesShown
#     cursor.execute("SELECT * FROM categories WHERE parent_id IS NULL LIMIT " +
#                    str(numberOfMainCategoriesShown + numberOfMainCategoriesToAdd))
#     mainCategories = cursor.fetchall()
#     numberOfMainCategoriesShown += numberOfMainCategoriesToAdd
#     return mainCategories


# def get_category():
#     global iDselectedCategory
#     cursor.execute("SELECT * FROM categories WHERE id=" +
#                    str(iDselectedCategory))
#     category = cursor.fetchall()
#     return category[0]


def get_products():
    cursor.execute("SELECT * FROM products")
    # cursor.execute("SELECT * FROM categories LIMIT 15 OFFSET 200")
    products = cursor.fetchall()
    return products


def get_number_of_products():
    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchall()
    return products


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
