# from bs4 import BeautifulSoup
# import requests
# import psycopg2
# from collections import deque

# TIKI_URL = 'https://tiki.vn/'

# # Access database
# conn = psycopg2.connect(user="felix",
#                         port="5432",
#                         database="tiki",
#                         password="felixpostgre")
# conn.autocommit = True
# cur = conn.cursor()

# def create_category_table():
#     query = """
#         CREATE TABLE IF NOT EXISTS categories(
#             id SERIAL PRIMARY KEY,
#             name VARCHAR(255),
#             url TEXT,
#             parent_id INT,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );
#     """
#     try:
#         cur.execute(query)
#     except Exception as err:
#         print(f'ERROR: {err}')

# create_category_table()
