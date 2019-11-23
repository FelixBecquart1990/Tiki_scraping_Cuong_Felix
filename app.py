from flask import Flask, render_template, request, redirect, url_for
import sql

app = Flask(__name__)


@app.route('/')
def index():
    categories = sql.get_categories(0)
    category = sql.get_category()
    numberOfCategories = sql.get_number_of_categories()
    return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories, category=category)


@app.route('/show-more-categories')
def show_more_categories():
    sql.numberOfCategoriesShown += 2
    return redirect(url_for('.index'))


@app.route("/get-category/<categoryId>", methods=['GET', 'POST'])
def get_category(categoryId):
    sql.iDselectedCategory = categoryId
    return redirect(url_for('.index'))


# @app.route('/test')
# def test():
#     categories = sql.get_categories(0)
#     numberOfCategories = sql.get_number_of_categories()
#     return render_template('index.html', categories=categories, numberOfCategories=numberOfCategories)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
