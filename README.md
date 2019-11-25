![Background](https://firebasestorage.googleapis.com/v0/b/vietnamesewithsophia.appspot.com/o/fond.JPG?alt=media&token=cae230b0-6728-43bc-b7b1-fa93134861a4)

# Project Tiki Scraping (Flask App & POSTGRE)

---

### Launch the app

```sh
# launch the application
python app.py
```

---

### Data architecture

| Products    | Type                        |
| ----------- | --------------------------- |
| id          | integer                     |
| title       | character varying(255)      |
| image       | text                        |
| category_id | integer                     |
| created_at  | timestamp without time zone |
| product_url | text                        |
| final_price | character varying(255)      |

| Categories | Type                        |
| ---------- | --------------------------- |
| id         | integer                     |
| name       | character varying(255)      |
| url        | text                        |
| parent_id  | integer                     |
| created_at | timestamp without time zone |

- Connect: We use psycopg2 LB to connect the python with PSQL. Change [User] and [Database] to yours to use this code
- Data collected: product title, brand name, old price, discount, final price, category, ratings, TikiNOW availability, image Url
- Take alook at [PhaCu_craw_code.ipynb] to see how to crawl all products from <tiki.vn>. We overcome the duplication of Product data by using the Categories Tree. In particular, we only get Product’s data from the deepest SubCategories, so the data is not duplicated.

---

### Example of scraping

```python
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
```

---

### Search method used

```python
# from app.py
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        productsToShow = products.get_search_products(form.search.data)
    else:
        productsToShow = products.get_products()

# from product.py
def get_search_products(search):
    cursor.execute("SELECT * FROM products WHERE title LIKE  '%" +
                   str(search) + "%' LIMIT 9")
    products = cursor.fetchall()
    return products
```

---

# Contact:

### Cuong & Félix

![Background](https://firebasestorage.googleapis.com/v0/b/vietnamesewithsophia.appspot.com/o/fond.JPG?alt=media&token=cae230b0-6728-43bc-b7b1-fa93134861a4)
