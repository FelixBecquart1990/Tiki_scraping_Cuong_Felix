import psycopg2
from bs4 import BeautifulSoup
import requests
from collections import deque
import categories

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
            category_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            product_url TEXT,
            final_price VARCHAR(255)
            );
    """
    try:
        cursor.execute(query)
    except Exception as err:
        print(f'ERROR: {err}')


class Product:
    def __init__(self, title, image, category_id, product_url, final_price):
        self.title = title
        self.image = image
        self.category_id = category_id
        self.product_url = product_url
        self.final_price = final_price

    def save_into_db(self):
        query = f"""
            INSERT INTO products (title, image, category_id, product_url, final_price)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        val = (self.title, self.image, self.category_id,
               self.product_url, self.final_price)
        try:
            cursor.execute(query, val)
        except Exception as err:
            print(f'ERROR: {err}')

    def __repr__(self):
        return f'ID: {self.product_id}, Name: {self.title}, Category_id: {self.category_id}'


def parse(url):
    try:
        response = requests.get(url).text
        response = BeautifulSoup(response, "html.parser")
        return response
    except Exception as err:
        print(f'ERROR: {err}')
        return ''


def crawl_products(url, category_id, save_db=False):

    try:
        div_containers = parse(url).find_all(
            'div', attrs={"class": "product-item"})
        # print(div_containers)
        if div_containers == []:
            return "no more products"
        for div in div_containers:
            title = div.get('data-title')
            image = div.img['src']
            # print(int(category_id))
            category_id = category_id,
            product_url = div.a['href']
            final_price = div.find(
                'span', class_='final-price').text.strip().split()[0]
            product = Product(title, image, category_id,
                              product_url, final_price)
            if save_db:
                product.save_into_db()
    except Exception as err:
        print(f'ERROR: {err}')

    return print("end of page crawling.")


def crawl_all_products_of_all_categories():
    allCategories = categories.get_all_categories()
    print(len(categories.get_all_categories()))
    print(type(categories.get_all_categories()))
    for category in allCategories:
        url = category[2]
        category_id = category[0]
        if url.find("page="):
            url = url[:url.find("&page=")]+"&page="
        else:
            url = a+"&page="
        i = 1
        while crawl_products(url+str(i), category_id, True) != "no more products":
            print("page " + str(i))
            i += 1


numberOfProductsToShow = 3


def get_products():
    cursor.execute("SELECT * FROM products WHERE category_id =" +
                   str(categories.iDselectedCategory) + " LIMIT " + str(numberOfProductsToShow))
    products = cursor.fetchall()
    return products


def get_search_products(search):
    cursor.execute("SELECT * FROM products WHERE title LIKE  '%" +
                   str(search) + "%' LIMIT 9")
    products = cursor.fetchall()
    return products


def get_number_of_products():
    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchall()
    return products


def get_number_of_products_of_category():
    cursor.execute("SELECT COUNT(*) FROM products WHERE category_id=" +
                   str(categories.iDselectedCategory))
    products = cursor.fetchall()
    return products
