from flask import Flask, render_template, request, redirect, url_for
import database
import crawl

app = Flask(__name__)


@app.route('/')
def index():
    database.create_category_table()
    category = database.get_category()
    mainCategories = database.get_main_categories(0)
    numberOfMainCategories = database.get_number_of_main_categories()
    subcategories = database.get_subcategories()
    return render_template('index.html', subcategories=subcategories, mainCategories=mainCategories, numberOfMainCategories=numberOfMainCategories, category=category)
    # return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories)
    # return render_template('index.html')


@app.route('/show-more-main-categories')
def show_more_main_categories():
    database.numberOfMainCategoriesShown += 2
    return redirect(url_for('.index'))


@app.route('/crawl-all-subcategories')
def crawl_all_subcategories():
    database.crawl_all_subcategories(database.crawl_main_categories())
    return redirect(url_for('.index'))

@app.route('/crawl-all-categories')
def crawl_all_categories():
    database.crawl_all_categories(database.crawl_main_categories())
    return redirect(url_for('.index'))

@app.route("/get-category/<categoryId>", methods=['GET', 'POST'])
def get_category(categoryId):
    database.iDselectedCategory = categoryId
    return redirect(url_for('.index'))


# @app.route('/test')
# def test():
#     categories = database.get_categories(0)
#     numberOfCategories = database.get_number_of_categories()
#     return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
