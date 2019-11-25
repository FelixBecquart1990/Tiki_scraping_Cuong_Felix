from flask import Flask, render_template, request, redirect, url_for
import categories
import products
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key'

# Form


class SearchForm(FlaskForm):
    search = StringField('Search for a product',
                         validators=[DataRequired()])
    submit = SubmitField('Search')

    def __repr__(self):
        return f"SearchForm('{self.search}')"


@app.route('/', methods=['GET', 'POST'])
def index():
    # if search, return result
    form = SearchForm()
    if form.validate_on_submit():
        productsToShow = products.get_search_products(form.search.data)
    # else, return products from selected category
    else:
        productsToShow = products.get_products()
    categories.create_categories_table()
    products.create_products_table()
    category = categories.get_category()
    mainCategories = categories.get_main_categories(0)
    subcategories = categories.get_subcategories()
    numberOfMainCategories = categories.get_number_of_main_categories()
    numberOfSubcategories = categories.get_number_of_subcategories()
    numberOfProducts = products.get_number_of_products()
    numberOfProductsOfCategory = products.get_number_of_products_of_category()
    return render_template('index.html', form=form, numberOfProductsOfCategory=numberOfProductsOfCategory, numberOfProducts=numberOfProducts, products=productsToShow, subcategories=subcategories, mainCategories=mainCategories, numberOfMainCategories=numberOfMainCategories, numberOfSubcategories=numberOfSubcategories, category=category)


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


@app.route('/crawl-all-products-of-all-categories')
def crawl_all_products_of_all_categories():
    products.crawl_all_products_of_all_categories()
    return redirect(url_for('.index'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
