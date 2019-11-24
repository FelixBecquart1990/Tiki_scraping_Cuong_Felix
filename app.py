from flask import Flask, render_template, request, redirect, url_for
import categories
import products

app = Flask(__name__)


@app.route('/')
def index():
    categories.create_categories_table()
    products.create_products_table()
    category = categories.get_category()
    mainCategories = categories.get_main_categories(0)
    subcategories = categories.get_subcategories()
    productsToShow = products.get_products()
    numberOfMainCategories = categories.get_number_of_main_categories()
    numberOfSubcategories = categories.get_number_of_subcategories()
    numberOfProducts = products.get_number_of_products()
    numberOfProductsOfCategory = products.get_number_of_products_of_category()
    return render_template('index.html', numberOfProductsOfCategory=numberOfProductsOfCategory, numberOfProducts=numberOfProducts, products=productsToShow, subcategories=subcategories, mainCategories=mainCategories, numberOfMainCategories=numberOfMainCategories, numberOfSubcategories=numberOfSubcategories, category=category)
    # return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories)
    # return render_template('index.html')


@app.route('/show-more-main-categories')
def show_more_main_categories():
    categories.numberOfMainCategoriesShown += 2
    return redirect(url_for('.index'))


@app.route('/crawl-all-subcategories')
def crawl_all_subcategories():
    categories.crawl_all_subcategories(categories.crawl_main_categories())
    return redirect(url_for('.index'))


@app.route('/crawl-all-categories')
def crawl_all_categories():
    categories.crawl_all_categories(categories.crawl_main_categories())
    return redirect(url_for('.index'))


@app.route("/get-subcategories/<categoryId>", methods=['GET', 'POST'])
def get_subcategories(categoryId):
    products.numberOfProductsToShow = 3
    categories.iDselectedCategory = categoryId
    return redirect(url_for('.index'))


@app.route("/get-products/<categoryId>", methods=['GET', 'POST'])
def get_products(categoryId):
    categories.iDselectedproducts = categoryId
    return redirect(url_for('.index'))


@app.route('/show-more-products')
def show_more_products():
    products.numberOfProductsToShow += 3
    return redirect(url_for('.index'))

# @app.route('/test-crawl-products')
# def test_crawl_products():
#     products.crawl_products(True)
#     return redirect(url_for('.index'))


@app.route('/crawl-all-products-of-all-categories')
def crawl_all_products_of_all_categories():
    products.crawl_all_products_of_all_categories()
    return redirect(url_for('.index'))
# @app.route('/test')
# def test():
#     categories = categories.get_categories(0)
#     numberOfCategories = categories.get_number_of_categories()
#     return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
