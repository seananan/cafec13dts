from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

DATABASE = "DB_FILE"

app = Flask(__name__)

def connect_database(db_file):
    """
    creates a connection to the database
    :param db_file:
    :return: conn
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")
    return



@app.route('/')
def render_homepage():  # put application's code here
    return render_template('home.html')


@app.route('/menu/<cat_id>')
def render_menu(cat_id):
    con = connect_database(DATABASE)
    query = "SELECT name, description, volume, image, price FROM products WHERE fk_cat_id = ?"
    query_cat_list = "SELECT * FROM category"
    cur = con.cursor()
    cur.execute(query, (cat_id,))
    product_list = cur.fetchall()
    cur.execute(query_cat_list)
    cat_list = cur.fetchall()
    print(product_list)
    print(cat_list)
    con.close()
    return render_template('menu.html', list_of_coffee=product_list, list_of_categories=cat_list)


@app.route('/login')
def render_login_page():  # put application's code here
    return render_template('login.html')


@app.route('/signup')
def render_signup_page():  # put application's code here
    return render_template('signup.html')




if __name__ == '__main__':
    app.run()
